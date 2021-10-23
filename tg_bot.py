import logging
import random
import time

from environs import Env
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.error import TimedOut, NetworkError

from utils import get_dg_flow_text, gc_session_id, gc_project_id, language_code, logger, TelegramLogsHandler

env = Env()
env.read_env()


def start(update, context):
    user = update.effective_user.full_name
    update.message.reply_text(
        text=f'Привет {user}!',
    )


def echo(update, context):
    answers = (
        'А вот это не совсем понятно.',
        'Вот сейчас я тебя совсем не понимаю.',
        'Попробуй, пожалуйста, выразить свою мысль по другому.',
        'Не совсем понимаю, о чём ты.',
        'Вот эта последняя фраза мне не ясна.'
    )
    dg_flow_text = get_dg_flow_text(gc_project_id, gc_session_id, update.message.text, language_code)
    if dg_flow_text:
        update.message.reply_text(dg_flow_text)
    else:
        update.message.reply_text(random.choice(answers))


def main():
    chat_id = env.str('CHAT_ID')
    updater = Updater(env.str('BOT_TOKEN'))
    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(chat_id))
    logger.warning('TG_Bot запущен.')
    while True:
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(MessageHandler(Filters.text, echo))
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
