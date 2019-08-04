import random
import sys
import io
import os
import vk_api
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
import time
from fetchdialogflow import fetch_dialogflow

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
                continue
            try:
                bot.send_message(chat_id=chat_id, text=log_entry)
                break
            except TimedOut:
                continue


def main():

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
                reply = fetch_dialogflow(event.user_id, event.text)
                if not reply['is_fallback']:
                    vk_api.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message=reply['text']
                            )
    except Exception as err:
        log.error('%s happend with VK bot(IT MIGHT BE DEAD!!)'%(err))
        time.sleep(15)


if __name__ == '__main__':
    main()
