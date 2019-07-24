import random
import sys
import io
import dialogflow
import os
import vk_api
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
import time


def make_logger(bot):

    log = logging.getLogger('Support_Bot')
    log.setLevel(logging.INFO)
    class Myhandler(logging.Handler):

      def emit(self, record):
        log_entry = self.format(record)
        while True:
            try:
                chat_id = bot.get_updates()[-1].message.chat_id
            except TimedOut:
                chat_id = None
            if chat_id is not None:
                try:
                    bot.send_message(chat_id=chat_id, text=log_entry)
                    break
                except TimedOut:
                    continue


def fetch_dialogflow(session_id, message, dialogflow_project_id):

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(dialogflow_project_id, session_id)

    text_input = dialogflow.types.TextInput(text=message, language_code='ru')
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise
    return response.query_result.fulfillment_text


if __name__ == "__main__":

    dialogflow_project_id = os.environ.get['DIALOGFLOW_PROJECT_ID']
    fallback_intent_phrases = [
    'Не совсем понимаю, о чём ты.',
    'Вот эта последняя фраза мне не ясна.',
    'А вот это не совсем понятно.',
    'Можешь сказать то же самое другими словами?',
    'Вот сейчас я тебя совсем не понимаю.',
    'Попробуй, пожалуйста, выразить свою мысль по-другому.'
    ]

    tg2_token = os.environ.get['TG2_TOKEN']
    vk_token = os.environ.get['VK_TOKEN']
    if tg2_token is None or vk_token is None:
        raise KeyError('One or more token is missing')

    dbgr_bot = telegram.Bot(token=tg2_token)
    log = make_logger(dbgr_bot)
    log.info('VK bot is up!')
    try:
        vk_session = vk_api.VkApi(token=vk_token)
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                reply = fetch_dialogflow(event.user_id, event.text, dialogflow_project_id)
                if reply not in fallback_intent_phrases:
                    vk_api.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message=reply
                            )
    except Exception as err:
        log.error('%s happend with VK bot(IT MIGHT BE DEAD!!)'%(err))
        time.sleep(15)
