import os
import json

from environs import Env
from google.cloud import dialogflow
from google.api_core.exceptions import InvalidArgument

env = Env()
env.read_env()


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)
    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)
    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )
    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )
    print("Intent created: {}".format(response))


def main():
    gc_project_id = env.str('GC_PROJECT_ID')
    with open("questions.json", "r", encoding='utf-8') as file:
        questions = json.load(file)
    for intent in questions:
        display_name = intent
        training_phrases_parts = questions[intent]['questions']
        message_texts = [questions[intent]['answer']]
        try:
            create_intent(gc_project_id, display_name, training_phrases_parts, message_texts)
        except InvalidArgument:
            continue


if __name__ == '__main__':
    main()
