import random

from environs import Env
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from utils import get_dg_flow_text, gc_session_id, gc_project_id, language_code

env = Env()


def echo(event, vk_api):
    dg_flow_text = get_dg_flow_text(gc_project_id, gc_session_id, event.text, language_code)
    vk_api.messages.send(
        user_id=event.user_id,
        message=dg_flow_text,
        random_id=random.randint(1, 1000)
    )


def main():
    vk_session = vk.VkApi(token=env.str('VK_TOKEN'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)


if __name__ == '__main__':
    main()
