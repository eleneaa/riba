from django.core.management.base import BaseCommand
from telegram import Bot, Update
from telegram.ext import CommandHandler, CallbackContext, Updater


class Command(BaseCommand):
    help = 'Starts the Telegram bot'

    def handle(self, *args, **kwargs):
        updater = Updater(token='7931952837:AAEZHM-KOo4fwV401YfQMhKP0iycGrD4woA', use_context=True)
        dispatcher = updater.dispatcher

        def start(update: Update, context: CallbackContext):
            update.message.reply_text('Hello! I am your bot.')

        start_handler = CommandHandler('start', start)
        dispatcher.add_handler(start_handler)

        updater.start_polling()
        updater.idle()

