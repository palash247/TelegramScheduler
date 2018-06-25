from flask_restful import Resource, reqparse
from models.group import GroupModel


class Group(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="Name of the group is required."
    )
    parser.add_argument(
        'chat_id',
        type=int,
        required=True,
        help='Chat id required.'
    )
    parser.add_argument(
        'time_zone',
        type=str,
        required=True,
        help='Time zone required.'
    )

    def get(self, name):
        group = GroupModel.find_by_name(name)
        if group:
            return group.json()
        return {'message': 'Group not found.'}

    def post(self, name):
        if GroupModel.find_by_name(name):
            return {'message': 'A Group with name {} already exists.'.format(name)}, 400

        request_data = Group.parser.parse_args()
        group = GroupModel(name, **request_data)
        try:
            group.save_to_db()
        except:
            return {'message': 'An error occured while inserting the group.'}
        return group.json(), 201

    def delete(self, name):
        group = GroupModel.find_by_name(name)
        if group:
            group.delete_from_db()
            return {'message': 'Deletion successful'}
        return {'message': 'Group not found'}, 401

    def put(self, name):
        request_data = Group.parser.parse_args()

        group = GroupModel.find_by_name(name)
        if group:
            group.time_zone = request_data['time_zone']
        else:
            group = GroupModel(name, **request_data)
        group.save_to_db()
        return group.json()


class GroupList(Resource):
    def get(self):
        return {'groups': list(map(lambda x: x.json, GroupModel.query.all()))}
