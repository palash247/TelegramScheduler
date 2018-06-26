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
    #     'group_id',
    #     type=int,
    #     required=True,
    #     help='No scheduled message exists without group_id'
    # )
    # def get(self, group_id, name):
    #     message = MessageModel.find_by_name_and_group(group_id=group_id, name=name)
    #     if message:
    #         return message.json()
    #     return {'message': 'Group_id and name combination does not exists.'}, 404

    def get(self, group_id):
        messages = MessageModel.query.filter_by(group_id=group_id)
        if len(messages) != 0:
            return list(map(lambda x: x.json(), messages))
        return {'message': 'The group_id does not exist.'}, 404

    def post(self, name, group_id):
        request_data = Message.parser.parse_args()
        message = MessageModel(name, group_id, **request_data)
        try:
            message.save_to_db()
        except:
            return {'message': 'Failed to insert message'}, 500
        return message.json(), 201

    def delete(self, group_id, name):

        message = MessageModel.find_by_name_and_group(
            name=name, group_id=group_id)
        if message:
            try:
                message.delete_from_db()
                return {'message': 'message deleted successfully'}
            except:
                return {'message': 'unable to delete the message'}, 500
        return {'message': 'resource does not exist.'}

    def put(self, name, group_id):
        request_data = Message.parser.parse_args()
        message = MessageModel.find_by_name_and_group(name, group_id)
        if message:
            message.text = request_data['text']
            message.schedule = request_data['schedule']
        else:
            message = MessageModel(name, group_id, **request_data)
        message.save_to_db()
        return message.json
