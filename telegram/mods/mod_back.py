# completed successfully ✅
import telegram
from telegram.core.bot.handler import CallbackHandler, CallbackQuery
from telegram.models import TelegramUser as User
from telegram.mods.menu import supperadmin_start, admin_start, user_start, unknown_starts

class BackToStratHandler(CallbackHandler):
    def callback_check(self, call: CallbackQuery) -> bool:
        return call.data == "back_to_start_menu"

    def user_handle(self, call: CallbackQuery, user: User):
        text, markup = user_start()
        self.bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            parse_mode="HTML",
            reply_markup=markup,

        )

    def admin_handle(self, call: CallbackQuery, user: User):
        text, markup = admin_start(user)
        self.bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            reply_markup=markup,
            parse_mode="HTML",
        )

    def superuser_handle(self, call: CallbackQuery, user: User):
        text, markup = supperadmin_start(user)
        self.bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            reply_markup=markup,
            parse_mode="HTML"
        )

class BackToNoIdUserStratHandler(CallbackHandler):
    def callback_check(self, call: CallbackQuery) -> bool:
        return call.data == "back_to_unknown_menu"

    def user_handle(self, call: CallbackQuery, user: User):
        text, markup = unknown_starts()
        self.bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            parse_mode="HTML",
            reply_markup=markup,

        )
