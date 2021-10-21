import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from utils import get_dg_flow_text, gc_session_id, gc_project_id, language_code


def start(update, context):
    user = update.effective_user.full_name
    update.message.reply_text(
        text=f'Привет {user}!',
    )


def echo(update, context):
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
