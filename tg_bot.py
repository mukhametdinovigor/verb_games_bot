import os

from google.cloud import dialogflow
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


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


def echo(update, context):
    gc_project_id = os.environ['GC_PROJECT_ID']
    gc_session_id = os.environ['GC_SESSION_ID']
    language_code = 'ru-RU'
    dg_flow_text = get_dg_flow_text(gc_project_id, gc_session_id, update.message.text, language_code)
    update.message.reply_text(dg_flow_text)


def main():
    updater = Updater(os.environ['BOT_TOKEN'])
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
