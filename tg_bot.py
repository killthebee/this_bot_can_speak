import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.error import TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError
import logging
from fetchdialogflow import fetch_dialogflow

TG1_TOKEN = os.environ.get['TG1_TOKEN']
TG2_TOKEN = os.environ.get['TG2_TOKEN']
if TG1_TOKEN is None or TG2_TOKEN is None:
     raise KeyError(
     'One of TOKENS is missing, you need to try launch this app one more time'
     )


class Log_mover():

    def __init__(self):
        self.log = None
    def login(self, log):
        self.log = log
    def logout(self):
        return self.log
the_log_mover = Log_mover()


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

    log.addHandler(Myhandler())
    return log
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)


def start(update, context):
    update.message.reply_text('Hello there!')


def mess(update, context):

    log = the_log_mover.logout()
    try:
        answer = fetch_dialogflow(update.message.chat_id, update.message.text)
        context.bot.send_message(chat_id=update.message.chat_id, text=answer['text'])
    except Exception as err:
        log.info('There is some issues with dialogflow')
        log.error(err, exc_info=True)


def error(update, context):

    log = the_log_mover.logout()
    log.info('Main bot experiencing %s', context.error)


def main():

    bot_dbgr = telegram.Bot(token=TG2_TOKEN)
    log = make_logger(bot_dbgr)
    the_log_mover.login(log)
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
