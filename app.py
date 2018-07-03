from flask import Flask, request, render_template, url_for, jsonify
from flask_jwt import JWT, jwt_required
from flask_restful import Api, Resource, reqparse
from security import authenticate, identity
from resourcess.group import Group, GroupList
from resourcess.message import Message, MessageList, MessageId
from resourcess.update import Update
from models.group import GroupModel
import os
import requests

TOKEN = os.environ.get('TELEGRAM_TOKEN')

app = Flask(__name__)
app.secret_key = 'palash'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///surveyor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True


@app.route('/')
def student():
   return render_template('student.html')

@app.route('/login', methods=['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      return render_template("result.html", result=result)

@app.route('/schedules')
def schedules():
    return render_template('schedules.html', groups=jsonify(requests.get('http://localhost:5000/groups')))
@app.route('/add_schedules', methods=["POST"])
def add_schedules():
    return render_template('add_schedule.html')
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


JWT(app, authenticate, identity)

api.add_resource(Group, '/group/<string:chat_id>')
api.add_resource(GroupList, '/groups')
# api.add_resource(Message, '/group/<string:chat_id>/message/<string:name>')
api.add_resource(MessageList, '/group/<string:chat_id>/messages')
api.add_resource(Update, '/{}'.format(TOKEN))
api.add_resource(Message, '/group/<string:chat_id>/message/<string:_id>')
api.add_resource(MessageId, '/group/<string:chat_id>/message')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
