import logging
import time

from google.cloud import dialogflow
from environs import Env
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.error import TimedOut, NetworkError

from tg_logs_handler import logger, TelegramLogsHandler

env = Env()
env.read_env()

gc_project_id = env.str('GC_PROJECT_ID')
gc_session_id = env.str('GC_SESSION_ID')
language_code = env.str('LANGUAGE_CODE')


def get_dg_flow_text(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result.fulfillment_text


def start(update, context):
    user = update.effective_user.full_name
    update.message.reply_text(
        text=f'Привет {user}!',
    )


def send_dg_flow_text(update, context):
    dg_flow_text = get_dg_flow_text(gc_project_id, gc_session_id, update.message.text, language_code)
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
