import logging
import time

from environs import Env
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.error import TimedOut, NetworkError

from dg_flow_api import get_dg_flow_text, GC_SESSION_ID
from tg_logs_handler import TelegramLogsHandler

logger = logging.getLogger('Logger')
env = Env()
env.read_env()

TG_GC_SESSION_ID = f"tg-{GC_SESSION_ID}"
GC_PROJECT_ID = env.str('GC_PROJECT_ID')
LANGUAGE_CODE = env.str('LANGUAGE_CODE')


def start(update, context):
    user = update.effective_user.full_name
    update.message.reply_text(
        text=f'Привет {user}!',
    )


def send_dg_flow_text(update, context):
    is_fallback, dg_flow_text = get_dg_flow_text(GC_PROJECT_ID, TG_GC_SESSION_ID, update.message.text, LANGUAGE_CODE)
    update.message.reply_text(dg_flow_text)


def main():
    chat_id = env.str('CHAT_ID')
    updater = Updater(env.str('BOT_TOKEN'))
    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(chat_id))
    logger.warning('TG_Bot запущен.')
    while True:
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(MessageHandler(Filters.text, send_dg_flow_text))
        try:
            updater.start_polling()
            updater.idle()
        except TimedOut:
            continue
        except NetworkError:
            logger.exception('Произошла ошибка')
            time.sleep(60)
            continue


if __name__ == '__main__':
    main()
