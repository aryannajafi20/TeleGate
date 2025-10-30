import logging
from telebot import TeleBot, types
from django.conf import settings
from telegram.core.bot.loader import load_handlers
from telegram.core.bot.handler import Handler  # your base class

logger = logging.getLogger(__name__)

# single global bot instance used everywhere
bot = TeleBot(settings.TELEGRAM_BOT_TOKEN)

# load and register handlers (load_handlers should not import views)
handlers = load_handlers(bot)

# Optional: a dispatcher function to be used by webhook or polling
def dispatch_message(message):
    """Run handlers in order until one handles the message."""
    for handler in handlers:
        if isinstance(handler, Handler) and handler.check(message):
            try:
                handler.handle(message)
            except Exception:
                logger.exception("Handler error")
            break

# If you prefer to use telebot decorators, you may also register them here:
@bot.message_handler(func=lambda m: True, chat_types=['private', 'channel'])
def _dispatcher(message):
    dispatch_message(message)