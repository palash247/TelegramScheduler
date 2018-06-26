from flask_restful import Resource, reqparse
from models.message import MessageModel


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
        type=float,
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
            chat_id=chat_id, name=name)
        if message:
            return message.json()
        return {'message': 'chat_id and name combination does not exists.'}, 404

    def post(self, name, chat_id):
        request_data = Message.parser.parse_args()
        print(request_data['text'], request_data['schedule'])
        message = MessageModel(name=name, chat_id=chat_id, **request_data)
        try:
            message.save_to_db()
        except:
            return {'message': 'Failed to insert message'}, 500
        return message.json(), 201

    def delete(self, chat_id, name):

        message = MessageModel.find_by_name_and_chat_id(
            name=name,
            chat_id=chat_id
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
            message = MessageModel(name=name, chat_id=chat_id, **request_data)
        message.save_to_db()
        return message.json()


class MessageList(Resource):

    def get(self, chat_id):
        messages = MessageModel.query.filter_by(chat_id=chat_id)
        if len(messages) != 0:
            return list(map(lambda x: x.json(), messages))
        return {'message': 'The chat_id does not exist.'}, 404
