import logging
import telegram
from telegram.error import TimedOut


class Telegram_handler(logging.Handler):

  def emit(self, record):

      tg2_token = os.environ.get['TG2_TOKEN']
      log_entry = self.format(record)
      bot = telegram.Bot(token=tg2_token)
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
