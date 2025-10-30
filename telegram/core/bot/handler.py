import logging
from abc import ABC, abstractmethod
from telebot import TeleBot
from telebot.types import Message, CallbackQuery
from telegram.models import TelegramUser as User, Status
from django.conf import settings

# ── Logging Configuration ─────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

def log_request(user: User, source: str, content: str, handler_name: str = ""):
    log_msg = (
        f"{'📝 Message' if source == 'message' else '🔘 Callback'}"
        f"{f' | 🔧 {handler_name}' if handler_name else ''} | "
        f"🆔 {user.chat_id} | 👤 @{user.username or 'N/A'} | "
        f"🏷 {user.telegram_name or 'N/A'} | "
        f"{'📝 Text' if source == 'message' else '📦 Data'}: {repr(content)}"
    )
    logger.info(log_msg)

# ──────────────────────────────────────────────────
# Base Message Handler
# ──────────────────────────────────────────────────
class Handler(ABC):
    def __init__(self, bot):
        self.bot: TeleBot = bot

    @abstractmethod
    def check(self, message: Message) -> bool:
        raise NotImplementedError("check method not implemented")

    def handle(self, message: Message):
        user, created = User.objects.get_or_create(
            chat_id=message.chat.id,
            defaults={
                "username": message.from_user.username,
                "telegram_name": f"{message.from_user.first_name} {message.from_user.last_name}",
                # "chat_id": message.chat.id,
                "is_active": True,
            }
        )
        if not user:
            return

        log_request(user, source="message", content=message.text, handler_name=self.__class__.__name__)

        if not user.is_active:
            return

        if user.is_superuser:
            self.superuser_handle(message, user)
            return
        status, created = Status.objects.get_or_create(defaults={'status': True}, token=settings.TELEGRAM_BOT_TOKEN)
        if status.status:
            if user.is_admin:
                self.admin_handle(message, user)
            else:
                self.user_handle(message, user)
        else:
            return

    def user_handle(self, message: Message, user: User):
        raise NotImplementedError("user_handle method is not implemented")

    def admin_handle(self, message: Message, user: User):
        raise NotImplementedError("admin_handle method is not implemented")

    def superuser_handle(self, message: Message, user: User):
        """Handle messages from superusers"""
        raise NotImplementedError("superuser_handle method is not implemented")

# ──────────────────────────────────────────────────
# Base Callback Handler
# ──────────────────────────────────────────────────
class CallbackHandler(ABC):
    def __init__(self, bot):
        self.bot: TeleBot = bot

    @abstractmethod
    def callback_check(self, call: CallbackQuery) -> bool:
        raise NotImplementedError("callback_check method not implemented")

    def handle(self, call: CallbackQuery):
        user, created = User.objects.get_or_create(
            chat_id=call.message.chat.id,
            defaults={
                "username": call.message.from_user.username,
                "telegram_name": f"{call.message.from_user.first_name} {call.message.from_user.last_name}",
                # "chat_id": call.message.chat.id,
                "is_active": True,
            }
        )
        if not user:
            return

        log_request(user, source="callback", content=call.data, handler_name=self.__class__.__name__)

        if not user.is_active:
            return

        if user.is_superuser:
            self.superuser_handle(call, user)
            return
        status, created = Status.objects.get_or_create(defaults={'status': True}, token=settings.TELEGRAM_BOT_TOKEN)
        if status.status:
            if user.is_admin:
                self.admin_handle(call, user)
            else:
                self.user_handle(call, user)
        else:
            return
    def user_handle(self, call: CallbackQuery, user: User):
        raise NotImplementedError("user_handle method is not implemented")

    def admin_handle(self, call: CallbackQuery, user: User):
        raise NotImplementedError("admin_handle method is not implemented")

    def superuser_handle(self, call: CallbackQuery, user: User):
        """Handle callbacks from superusers"""
        raise NotImplementedError("superuser_handle method is not implemented")

