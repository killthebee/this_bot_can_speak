import os
import logging
import logging.config
import tg_bot
import vk_bot
import scriptteacher
import argparse

loggingdict = {
    'version': 1,
    'handlers': {
        'bot_handler': {
            'class': 'log_module.Telegram_handler',
            'formatter': 'tg_formatter'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console_formatter'
        }
    },
    'loggers': {
        'bot_logger': {
            'handlers': ['bot_handler', 'console'],
            'level': 'INFO'
        }
    },
    'formatters': {
        'tg_formatter': {
            'format': '%(message)s'
        },
        'console_formatter': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    }
}

logging.config.dictConfig(loggingdict)

parser = argparse.ArgumentParser(
    description='Choose what i should launch'
)
parser.add_argument('app', help='Input VK or TG')
parser.add_argument('-t', '--to_teach', help='Write Yes if you need to teach bot some phrases')
args = parser.parse_args()

if args.to_teach == 'Yes':
    scriptteacher.main()
if args.app == 'VK':
    vk_bot.main()
elif args.app == 'TG':
    tg_bot.main()
else:
    print('You should write VK or TG after launcher.py')
