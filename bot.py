import os

from telegram import ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


def start(update, context):
    user = update.effective_user.full_name
    update.message.reply_text(
        text=f'Привет {user}!',
        # reply_markup=ForceReply(selective=True),
    )


def echo(update, context):
    update.message.reply_text(update.message.text)


def main():
    updater = Updater(os.environ['BOT_TOKEN'])
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
