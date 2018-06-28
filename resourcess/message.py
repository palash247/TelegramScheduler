
import sys
import os
import datetime
from dateutil.parser import parse
from apscheduler.job import Job
from scheduler import scheduler

from models.message import MessageModel
from models.group import GroupModel
from flask_restful import Resource, reqparse
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO, filename='log/messages.log')

logger = logging.getLogger()


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
    # parser.add_argument(
    #     'chat_id',
    #     type=int,
    #     required=True,
    #     help='No scheduled message exists without chat_id'
    # )

    def get(self, chat_id, name):
        message = MessageModel.find_by_name_and_chat_id(
            chat_id=int(chat_id), name=name)
        if message:
            return message.json()
        return {'message': 'chat_id and name combination does not exists.'}, 404

    def post(self, name, chat_id):
        
        request_data = Message.parser.parse_args()
        logger.info("Received schedule {} for message {}".format(
            request_data['text'],
            request_data['schedule']
            )
        )
        schedule = parse(request_data['schedule'])
        if schedule < datetime.datetime.now():
            return {'message':'You can not schedule a message in past'}, 400
        
        try:
            _id = Job(scheduler).id
            from resourcess.update import Update
            job = scheduler.add_job(
                id = _id,
                func=Update.send_message,
                trigger='date',
                args=[request_data['text'], int(chat_id), _id]
                )
            # if unable to add to job to scheduler don't add it to messages.
            message = MessageModel(
                _id=job.id,
                name=name,
                chat_id=int(chat_id),
                **request_data
                )
            message.save_to_db()
        except:
            return {'message': 'Failed to insert message'}, 500
        return message.json(), 201

    def delete(self, chat_id, name):

        message = MessageModel.find_by_name_and_chat_id(
            name=name,
            chat_id=int(chat_id)
        )
        if message:
            try:
                message.delete_from_db()
                return {'message': 'message deleted successfully'}
            except:
                return {'message': 'unable to delete the message'}, 500
        return {'message': 'resource does not exist.'}

    def put(self, name, chat_id):
        request_data = Message.parser.parse_args()
        message = MessageModel.find_by_name_and_group(name, chat_id)
        if message:
            message.text = request_data['text']
            message.schedule = request_data['schedule']
        else:
            message = MessageModel(
                name=name, chat_id=int(chat_id), **request_data)
        message.save_to_db()
        return message.json()


class MessageList(Resource):

    def get(self, chat_id):
        messages = MessageModel.query.filter_by(chat_id=int(chat_id))
        if messages:
            return list(map(lambda x: x.json(), messages))
        return {'message': 'The chat_id does not exist.'}, 404
