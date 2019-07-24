import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.error import TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError
import logging
import dialogflow
from google.api_core.exceptions import InvalidArgument


TG1_TOKEN = os.environ.get('TG1_TOKEN')
TG2_TOKEN = os.environ.get('TG2_TOKEN')
DIALOGFLOW_PROJECT_ID= os.environ.get('DIALOGFLOW_PROJECT_ID')
if TG1_TOKEN is None or TG2_TOKEN is None:
     raise KeyError(
     'One of TOKENS is missing, you need to try launch this app one more time'
     )


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

    log.addHandler(Myhandler())
    return log
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
bot_dbgr = telegram.Bot(token=TG2_TOKEN)
log = make_logger(bot_dbgr)


def fetch_dialogflow(session_id, message):

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, session_id)

    text_input = dialogflow.types.TextInput(text=message, language_code='ru')
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise
    return response.query_result.fulfillment_text


def start(update, context):
    update.message.reply_text('Hello there!')

def mess(update, context):
    try:
        answer = fetch_dialogflow(update.message.chat_id, update.message.text)
    except Exception as err:
        log.info('There is some issues with dialogflow')
        log.error(err, exc_info=True)
    context.bot.send_message(chat_id=update.message.chat_id, text=answer)


def error(update, context):

    log.info('Main bot experiencing %s', context.error)



def main():

    updater = Updater(TG1_TOKEN, use_context = True)
    log.info('bot is up!')
    dp = updater.dispatcher
    dp.add_error_handler(error)
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, mess))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
