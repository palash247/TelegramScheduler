
from flask_restful import Resource, request
import requests
from models.group import GroupModel
import logging
import os
from models.message import MessageModel
from models.schedule import ScheduleModel
from models.user import UserModel
from models.telegram import TelegramModel
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
            telegram_group = TelegramModel.find_by_group_chat_id(
                data[MESSAGE][CHAT][ID])
            group = GroupModel.find_by_id(telegram_group.group_fk)
            if group:
                logger.info('Group already exists in the database')
                return None
            group = GroupModel(data[MESSAGE][CHAT][TITLE],data[MESSAGE][CHAT][ID])
            telegram = TelegramModel(
                data[MESSAGE][CHAT][ID], data[MESSAGE][CHAT][TITLE],group.id)
            try:
                group.save_to_db()
                telegram.save_to_db()
                logger.info('Group added to database')
            except:
                logger.error('unable to add group to database')
        
        if self._is_removed(data):
            # remove group from db
            telegram_group = TelegramModel.find_by_group_chat_id(
                data[MESSAGE][CHAT][ID])
            group = GroupModel.find_by_id(telegram_group.group_fk)
            if group:
                group.delete_from_db()
                telegram_group.delete_from_db()
                logger.info('Group successfully deleted from database')
            else:
                logger.warning('Delete executed on a group which does not exist in the database.')
        

        if self._is_title_changed(data):
            telegram_group = TelegramModel.find_by_group_chat_id(
                data[MESSAGE][CHAT][ID])
            telegram_group.group_name = data[MESSAGE][CHAT][NEW_CHAT_TITLE]
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
    def telegram_send_message(cls, text, chat_id):
        url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
        cls.get_url(url)

    @classmethod
    def get_url(cls, url):
        response = requests.get(url)
        content = response.content.decode("utf8")
        return content

    # This method is used to send the message to the individual person or a group
    # will return true if the message has been sent, false else

    @classmethod
    def whatsapp_send_message(cls, name, message):
        # this will emojify all the emoji which is present as the text in string
        from whatsapp import whatsapp
        import time
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.common.exceptions import NoSuchElementException
        from selenium.common.exceptions import TimeoutException
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.keys import Keys
        message = whatsapp.emojify(message)
        search = whatsapp.browser.find_element_by_xpath(
            '/html/body/div[1]/div/div/div[2]/div/div[2]/div/label/input')
        # we will send the name to the input key box
        search.send_keys(name+Keys.ENTER)
        current_time = time.time()
        try:
            send_msg = WebDriverWait(whatsapp.browser, whatsapp.timeout).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/div/div/div[3]/div/footer/div[1]/div[2]/div/div[2]")))
            send_msg.send_keys(message+Keys.ENTER)  # send the message
            return True
        except TimeoutException:
            raise TimeoutError(
                "Your request has been timed out! Try overriding timeout!")
        except NoSuchElementException:
            return False
        except Exception:
            return False
            
        
