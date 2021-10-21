import random
import os

from google.cloud import dialogflow
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType


def get_dg_flow_text(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result.fulfillment_text


def echo(event, vk_api):
    gc_project_id = os.environ['GC_PROJECT_ID']
    gc_session_id = os.environ['GC_SESSION_ID']
    language_code = 'ru-RU'
    dg_flow_text = get_dg_flow_text(gc_project_id, gc_session_id, event.text, language_code)
    vk_api.messages.send(
        user_id=event.user_id,
        message=dg_flow_text,
        random_id=random.randint(1, 1000)
    )


def main():
    vk_session = vk.VkApi(token=os.environ['VK_TOKEN'])
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)


if __name__ == '__main__':
    main()
