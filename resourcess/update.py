
from flask_restful import Resource, request
from models.group import GroupModel

BOT_USERNAME = "ConsumerSurveyorBot"
NEW_CHAT_PARTICIPANT = "new_chat_participant"
USERNAME = "username"
LEFT_CHAT_PARTICIPANT = 'left_chat_participant'
CHAT_ID = 'chat_id'


class Update(Resource):

    def post(self):
        if self._if_added():
            # add new group to db
            pass

        if self._if_removed():
            # remove group from db
            pass

    def _if_added(self):
        """ 
        Returns True if added to new group, False otherwise.
        """
        data = request.get_json()
        if NEW_CHAT_PARTICIPANT in data:
            if BOT_USERNAME == data[NEW_CHAT_PARTICIPANT][USERNAME]:
                return True

    def _if_removed(self):
        """
        Returns True if removed from account, False otherwise.
        """
        data = request.get_json()
        if LEFT_CHAT_PARTICIPANT in data:
            if BOT_USERNAME in data[LEFT_CHAT_PARTICIPANT][USERNAME]:
                return True

    def _save_to_db(self, chat_id, group_name):
        """
        Save chat ids to the db
        """
        group = GroupModel(group_name, chat)
