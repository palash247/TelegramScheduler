
from flask_restful import Resource, request
import requests
from models.group import GroupModel
import logging
import os
from models.message import MessageModel
from models.schedule import ScheduleModel
from models.user import UserModel
logging.basicConfig(
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
logger = logging.getLogger()

BOT_USERNAME = "ConsumerSurveyorBot"
NEW_CHAT_PARTICIPANT = "new_chat_participant"
USERNAME = "username"
LEFT_CHAT_PARTICIPANT = 'left_chat_participant'
CHAT = 'chat'
ID = 'id'
TITLE = 'title'
TIME_ZONE = 'Asia/Kolkata'
MESSAGE = 'message'
PRIVATE = 'private'
TYPE = 'type'
NEW_CHAT_TITLE = 'new_chat_title'
TOKEN = os.environ.get('TELEGRAM_TOKEN')


URL = "https://api.telegram.org/bot{}/".format(TOKEN)

class Update(Resource):

    def post(self):
        data = request.get_json()
        if self._is_added(data):
            """
            Add new group to DB
            """
            group = GroupModel.find_by_chat_id(data[MESSAGE][CHAT][ID])
            if group:
                logger.info('Group already exists in the database')
                return None
            group = GroupModel(data[MESSAGE][CHAT][TITLE],data[MESSAGE][CHAT][ID],TIME_ZONE)
            try:
                group.save_to_db()
                logger.info('Group added to database')
            except:
                logger.error('unable to add group to database')
        
        if self._is_removed(data):
            # remove group from db
            group = GroupModel.find_by_chat_id(data[MESSAGE][CHAT][ID])
            if group:
                group.delete_from_db()
                logger.info('Group successfully deleted from database')
            else:
                logger.warning('Delete executed on a group which does not exist in the database.')
        

        if self._is_title_changed(data):
            group = GroupModel.find_by_chat_id(data[MESSAGE][CHAT][ID])
            group.name = data[MESSAGE][CHAT][NEW_CHAT_TITLE]
            try:
                group.save_to_db()
                logger.info('Group title updated.')
            except:
                logger.error('Failed to update Group title to {}'.format(
                    data[MESSAGE][CHAT][NEW_CHAT_TITLE]))

    def _is_added(self, data):
        """ 
        Returns True if added to new group, False otherwise.
        """
        if NEW_CHAT_PARTICIPANT in data[MESSAGE]:
            if USERNAME in data[MESSAGE][NEW_CHAT_PARTICIPANT]:
                if BOT_USERNAME == data[MESSAGE][NEW_CHAT_PARTICIPANT][USERNAME]:
                    return True 
        return False

    def _is_removed(self, data):
        """
        Returns True if removed from account, False otherwise.
        """

        if LEFT_CHAT_PARTICIPANT in data[MESSAGE]:
            if USERNAME in data[MESSAGE][LEFT_CHAT_PARTICIPANT]:
                if BOT_USERNAME in data[MESSAGE][LEFT_CHAT_PARTICIPANT][USERNAME]:
                    return True
        return False

    def _is_title_changed(self, data):
        """
        Returns tru if title of the group is changed.
        """
        if NEW_CHAT_TITLE in data[MESSAGE][CHAT]:
            return True
        return False


    @classmethod
    def send_message(cls, text, chat_id):
        url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
        cls.get_url(url)

    @classmethod
    def get_url(cls, url):
        response = requests.get(url)
        content = response.content.decode("utf8")
        return content
        
    
