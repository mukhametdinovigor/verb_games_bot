import logging
import random
import time

from google.cloud import dialogflow
from environs import Env
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.exceptions import ApiHttpError
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
    if not response.query_result.intent.is_fallback:
        return response.query_result.fulfillment_text


def send_dg_flow_text(event, vk_api):
    dg_flow_text = get_dg_flow_text(gc_project_id, gc_session_id, event.text, language_code)
    if dg_flow_text:
        vk_api.messages.send(
            user_id=event.user_id,
            message=dg_flow_text,
            random_id=random.randint(1, 1000)
        )
    pass


def main():
    chat_id = env.str('CHAT_ID')
    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(chat_id))
    logger.warning('VK_Bot запущен.')
    while True:
        try:
            vk_session = vk.VkApi(token=env.str('VK_TOKEN'))
            vk_api = vk_session.get_api()
            longpoll = VkLongPoll(vk_session)
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    echo(event, vk_api)
        except ApiHttpError:
            logger.exception('Произошла ошибка')
            time.sleep(60)
            continue


if __name__ == '__main__':
    main()
