import random
import logging
import sys
import io
import os
import vk_api
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
import time
from fetchdialogflow import fetch_dialogflow


def main():

    vk_token = os.environ.get['VK_TOKEN']
    if vk_token is None:
        raise KeyError('One or more tokens is missing')

    log = logging.getLogger('bot_logger')
    log.info('VK bot is up!')
    try:
        vk_session = vk_api.VkApi(token=vk_token)
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                reply = fetch_dialogflow(event.user_id, event.text)
                if reply['is_fallback']:
                    log.info(
                        'Bip-bop. I need your help with this message: \n%s'%(event.text)
                    )
                elif not reply['is_fallback']:
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
