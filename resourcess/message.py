
import sys
import os
import datetime
import traceback
from dateutil.parser import parse
from apscheduler.job import Job
from scheduler import scheduler

from models.message import MessageModel
from models.group import GroupModel
from flask_restful import Resource, reqparse
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)

logger = logging.getLogger('messages')


def schedule_msg(text, schedule, chat_id, job=None):
    from resourcess.update import Update
    if job:
        job.modify(
            func=Update.send_message,
            run_date=schedule,
            trigger='date',
            args=[text, int(chat_id)]
        )
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


def delete_schedule(job):
        job.remove()
# class Message(Resource):
#     parser = reqparse.RequestParser()
#     parser.add_argument(
#         'text',
#         type=str,
#         required=True,
#         help='Text message required.'
#     )
#     parser.add_argument(
#         'schedule',
#         type=str,
#         required=True,
#         help='Schedule of the message is required.'
#     )
#     parser.add_argument(
#         'name',
#         type=str,
#         required=True,
#         help='It will help you to access/understand the scheduled messages if you name them.'

#     )

#     def get(self, chat_id, name):
#         message = MessageModel.find_by_name_and_chat_id(
#             chat_id=int(chat_id), name=name)
#         if message:
#             return message.json()
#         return {'message': 'chat_id and name combination does not exists.'}, 404

#     def post(self, name, chat_id):

#         request_data = Message.parser.parse_args()
#         logger.info("Received schedule {} for message {}".format(
#             request_data['text'],
#             request_data['schedule']
#         )
#         )
#         schedule = parse(request_data['schedule'])
#         if schedule < datetime.datetime.now():
#             return {'message': 'You can not schedule a message in past'}, 400

#         try:
#             _id = Job(scheduler).id
#             from resourcess.update import Update
#             scheduler.add_job(
#                 id=_id,
#                 func=Update.send_message,
#                 run_date=request_data['schedule'],
#                 trigger='date',
#                 args=[request_data['text'], int(chat_id), _id]
#             )
#             # if unable to add to job to scheduler don't add it to messages.
#             message = MessageModel(
#                 id=_id,
#                 name=name,
#                 chat_id=int(chat_id),
#                 **request_data
#             )
#             message.save_to_db()
#         except Exception as e:
#             logger.error(traceback.format_exc())
#             return {'message': 'Failed to insert message'}, 500
#         return message.json(), 201

#     def delete(self, chat_id, name):

#         message = MessageModel.find_by_name_and_chat_id(
#             name=name,
#             chat_id=int(chat_id)
#         )
#         if message:
#             try:
#                 [msg.delete_from_db() for msg in message]
#                 return {'message': 'message deleted successfully'}
#             except Exception as e:
#                 logger
#                 return {'message': 'unable to delete the message'}, 500
#         return {'message': 'resource does not exist.'}

#     def put(self, name, chat_id):
#         request_data = Message.parser.parse_args()
#         message = MessageModel.find_by_name_and_group(name, chat_id)
#         if message:
#             message.text = request_data['text']
#             message.schedule = request_data['schedule']
#         else:
#             message = MessageModel(
#                 name=name, chat_id=int(chat_id), **request_data)
#         message.save_to_db()
#         return message.json()


class MessageList(Resource):

    def get(self, chat_id):
        messages = MessageModel.query.filter_by(chat_id=int(chat_id))
        if messages:
            return list(map(lambda x: x.json(), messages))
        return {'message': 'The chat_id does not exist.'}, 404


class Message(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'text',
        type=str,
        required=True,
        help='Text message required.'
    )
    parser.add_argument(
        'schedule',
        type=str,
        required=True,
        help='Schedule of the message is required.'
    )
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help='It will help you to access/understand the scheduled messages if you name them.'

    )
    parser.add_argument(
        'id',
        type=str
    )


    def get(self, chat_id, id):
        message = MessageModel.find_by_id(_id=id, chat_id=chat_id)
        if message:
            return message.json()
        return {'message': 'No scheduled message found for id {}'.format(id)}, 404

    def delete(self, chat_id, _id):
        message = MessageModel.find_by_id(_id=_id, chat_id=chat_id)
        job = scheduler.get_job(_id)
        if message and job:
            try:
                delete_schedule(job)
                # message.delete_from_db() this should be automatically handled by the trigger on apschedule_jobs table
                return {'message': 'Scheduled message successfully deleted.'}
            except:
                return {'message': 'Unable to delete the message'}
        return {'message': 'No scheduled message found for id {}'.format(_id)}, 400

    def put(self, chat_id, _id):
        request_data = MessageId.parser.parse_args()
        schedule = parse(request_data['schedule'])
        if schedule < datetime.datetime.now():
            return {'message': 'You can not schedule a message in past'}, 400
        job = scheduler.get_job(request_data['id'])
        message = MessageModel.find_by_id(
            _id=request_data['id'], chat_id=chat_id)
        if job and message:
            schedule_msg(
                request_data['text'], request_data['schedule'], chat_id, job)
            message['name'] = request_data['name']
            message['text'] = request_data['text']
            message['schedule'] = request_data['schedule']
            message.save_to_db()
            return message.json(), 204
        return {'message': 'Scheduled message with the id {} does not exists.'.format(request_data['id'])}, 400


class MessageId(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'text',
        type=str,
        required=True,
        help='Text message required.'
    )
    parser.add_argument(
        'schedule',
        type=str,
        required=True,
        help='Schedule of the message is required.'
    )
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help='It will help you to access/understand the scheduled messages if you name them.'

    )
    parser.add_argument(
        'id',
        type=str
    )

    def post(self, chat_id):
        request_data = MessageId.parser.parse_args()
        schedule = parse(request_data['schedule'])
        if schedule < datetime.datetime.now():
            return {'message': 'You can not schedule a message in past'}, 400
        job = schedule_msg(request_data['text'],
                           request_data['schedule'], chat_id)
        message = MessageModel(
            job.id, request_data['name'], request_data['text'], request_data['schedule'], chat_id)
        message.save_to_db()
        return message.json(), 200
