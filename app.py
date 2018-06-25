from flask import Flask, jsonify, request
from flask_jwt import JWT, jwt_required
from flask_restful import Api, Resource
from security import authenticate, identity

app = Flask(__name__)
api = Api(app)

jwt = JWT(app, authenticate, identity)


class Group(Resource):
    def get(self, name):
        return {"group": name}


api.add_resource(Group, '/group/<string:name>')

groups = [
    {
        "name": "Demo",
        "chat_id": 123,
        "time_zone": "Asia/Kolkata",
        "messages": [
            {
                "text": "hello world",
                "schedule": 1529908499.7678914
            }
        ]
    }
]

# create group


@app.route('/group', methods=['POST'])
def create_group():
    request_data = request.get_json()
    new_group = {
        'name': request_data['name'],
        'chat_id': request_data['chat_id'],
        'time_zone': request_data['time_zone'],
        'messages': []
    }
    groups.append(new_group)
    return jsonify(new_group)
# get groupe by name


@app.route('/group/<string:name>', methods=['GET'])
def get_group(name):
    for group in groups:
        if name == group['name']:
            return jsonify(group)
    return jsonify({'message': 'Group not found'})

# get all groups


@app.route('/group', methods=['GET'])
def get_groups():
    return jsonify({"groups": groups})

# create messages accourding to group


@app.route('/group/<string:name>/message', methods=['POST'])
def create_msg_in_group(name):
    request_data = request.get_json()
    for group in groups:
        if name == group['name']:
            new_message = {
                'text': request_data['text'],
                'schedule': request_data['schedule']
            }
            group['messages'].append(new_message)
            return jsonify(new_message)
    return jsonify({'message': 'group not found'})

# get msg by group name


@app.route('/group/<string:name>/messages', methods=['GET'])
def get_msgs_in_group(name):
    for group in groups:
        if name == group['name']:
            return jsonify(group['messages'])
    return jsonify({'message': 'group not found'})


app.run(port=5000)
