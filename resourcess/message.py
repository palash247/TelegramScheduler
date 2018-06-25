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
    parser.add_argument(
        'group_id',
        type=int,
        required=True,
        help='No scheduled message exists without group_id'
    )

    def get(self, name, group_id):
        message =

    def post(self):
        request_data = Message.parser.parse_args()
        message = MessageModel(**request_data)
        try:
            message.save_to_db()
        except:
            return {'message': 'Failed to insert message'}, 500
        return message.json(), 201

    def delete(self)
