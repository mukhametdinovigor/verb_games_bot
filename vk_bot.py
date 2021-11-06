import logging
import random
import time

from environs import Env
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.exceptions import ApiHttpError

from dg_flow_api import get_dg_flow_text
from tg_logs_handler import TelegramLogsHandler

logger = logging.getLogger('Logger')
env = Env()
env.read_env()

GC_PROJECT_ID = env.str('GC_PROJECT_ID')
LANGUAGE_CODE = env.str('LANGUAGE_CODE')


def send_dg_flow_text(event, vk_api):
    vk_gs_session_id = f"vk-{event.user_id}"
    is_fallback, dg_flow_text = get_dg_flow_text(GC_PROJECT_ID, vk_gs_session_id, event.text, LANGUAGE_CODE)
    if not is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=dg_flow_text,
            random_id=random.randint(1, 1000)
        )


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
                    send_dg_flow_text(event, vk_api)
        except ApiHttpError:
            logger.exception('Произошла ошибка')
            time.sleep(60)
            continue


if __name__ == '__main__':
    main()
