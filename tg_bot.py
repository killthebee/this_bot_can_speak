import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.error import TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError
import logging
from fetchdialogflow import fetch_dialogflow

TG1_TOKEN = os.environ.get['TG1_TOKEN']
if TG1_TOKEN is None:
     raise KeyError(
        'One of TOKENS is missing, you need to try launch this app one more time'
     )


log = logging.getLogger('bot_logger')


def start(update, context):
    update.message.reply_text('Hello there!')


def mess(update, context):

    try:
        answer = fetch_dialogflow(update.message.chat_id, update.message.text)
        context.bot.send_message(chat_id=update.message.chat_id, text=answer['text'])
    except Exception as err:
        log.info('There is some issues with dialogflow')
        log.error(err, exc_info=True)


def error(update, context):

    log.info('Main bot experiencing %s', context.error)


def main():

    log.info('bot is up')
    updater = Updater(TG1_TOKEN, use_context = True)
    dp = updater.dispatcher
    dp.add_error_handler(error)
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, mess))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
