from django.core.management.base import BaseCommand
from telegram.core.bot.bot import bot

class Command(BaseCommand):
    help = "Describe what this command does"

    def handle(self, *args, **options):
        try:
            bot.infinity_polling()
        except Exception as e:
            print(e)
