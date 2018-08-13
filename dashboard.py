from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from auth import login_required
from db import db
from models.group import GroupModel
import datetime
from dateutil.parser import parse
from models.message import MessageModel
from models.whatsapp import WhatsAppModel
from models.telegram import TelegramModel
from apscheduler.job import Job
from scheduler import scheduler
import pytz
from whatsapp import whatsapp

bp = Blueprint('dashboard', __name__)


def delete_schedule(job):
        job.remove()

def schedule_msg(text, schedule, chat_id, job=None):
    from resourcess.update import Update
    if job:
        job.modify(
            func=Update.send_message,
            args=[text, int(chat_id)]
        )
        if schedule != job.next_run_time:
            job.reschedule(trigger='date',run_date=schedule )
        return job
    else:
        _id = Job(scheduler).id
        job = scheduler.add_job(
            id=_id,
            func=Update.send_message,
            run_date=schedule,
            trigger='date',
            args=[text, int(chat_id)]
        )
        return job

@bp.route('/')
@login_required
def index():
    """Show all the groups."""
    groups = list(map(lambda x: x.json(), GroupModel.query.all()))  
    return render_template('dashboard/schedules.html', groups=groups)


@bp.route('/add_schedule', methods=['POST','GET'])
@login_required
def add_schedule():
    """ Schedule a message for a group """
    if request.method == 'GET':
        whatsapp.check_update()
        groups = list(map(lambda x: x.json(), GroupModel.query.all()))
        if len(groups) == 0 :
            
            flash("It seems you have not added the @ConsumerSurveyorBot to any group of any channel. Please, add the the bot to any group to schedule the message for the same.")
            return redirect(url_for('dashboard.index'))
        return render_template('dashboard/add_schedule.html', groups = groups)

    if request.method == 'POST':

        error = None
        schedule = parse(request.form['schedule']+'+05:30')
        if schedule < datetime.datetime.now(pytz.timezone('Asia/Kolkata')):
            error = 'You can not schedule a message in past'
        if error is not None:
            flash(error)
        else:
                
            job = schedule_msg(request.form['message'],
                            schedule, request.form['group_id'])
            message = MessageModel( 
                job.id, request.form['name'], request.form['message'], request.form['schedule']+'+05:30', request.form['group_id']   )
            message.save_to_db()
            return redirect(url_for('dashboard.index')) 
    return render_template('dashboard/add_schedule.html')


@bp.route('/update/<string:chat_id>/<string:id>', methods=('GET', 'POST'))
@login_required
def update(chat_id,id):
    if request.method == 'GET':
        message = MessageModel.find_by_id(chat_id, id)
        if message is None:
            flash('The scheduled message is already executed or does not exists.')
            return redirect(url_for('dashboard.index'))
        group = GroupModel.find_by_chat_id(chat_id=chat_id)
        return render_template('dashboard/update.html', message = message, group_name=group.name)
    if request.method == "POST":
        chat_id = int(chat_id)
        schedule = parse(request.form['schedule']+'+05:30')
        error = None
        if schedule < datetime.datetime.now(pytz.timezone('Asia/Kolkata')):
            error = 'You can not schedule a message in past'
        if error:
            flash(error)
        job = scheduler.get_job(id)
        message = MessageModel.find_by_id(
            _id=id, group_id=chat_id)
        if job and message:
            schedule_msg(
                request.form['text'], schedule, chat_id, job)
            message.name = request.form['name']
            message.text = request.form['text']
            message.schedule = request.form['schedule']+'+05:30'
            message.save_to_db()
            return redirect(url_for('dashboard.index'))
    return render_template('dashboard/schedules.html')


@bp.route('/update/<string:chat_id>/<string:id>', methods=( 'POST',))
@login_required
def delete():
    message = MessageModel.find_by_id(_id=request.form['id'], chat_id=request.form['chat_id'])
    job = scheduler.get_job(request.form['id'])
    if message and job:
        try:
            delete_schedule(job)
            # message.delete_from_db() this should be automatically handled by the trigger on apschedule_jobs table
            return redirect(url_for('dashboard.index'))
        except:
            flash('Unable to delete the message')
    flash('No scheduled message found for id {}'.format(request.form['id']))
