import logging

from environs import Env
from google.cloud import dialogflow
import telegram

logger = logging.getLogger('Logger')

env = Env()
env.read_env()


class TelegramLogsHandler(logging.Handler):
    def __init__(self, chat_id):
        super().__init__()
        tg_bot = telegram.Bot(token=env.str('BUG_REPORTING_BOT_TOKEN'))
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


gc_project_id = env.str('GC_PROJECT_ID')
gc_session_id = env.str('GC_SESSION_ID')
language_code = 'ru-RU'


def get_dg_flow_text(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    if not response.query_result.intent.is_fallback:
        return response.query_result.fulfillment_text
