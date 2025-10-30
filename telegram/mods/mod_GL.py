# completed successfully ✅
from telegram.core.bot.handler import CallbackHandler, CallbackQuery
from telegram.models import TelegramUser as User
from telegram.mods.menu import super_admin_generate_link, admin_generate_link


class GenerateLinkCallbackHandler(CallbackHandler):
    def callback_check(self, call: CallbackQuery) -> bool:
        return call.data == "generate_link"

    def user_handle(self, call: CallbackQuery, user: User):
        pass

    def admin_handle(self, call: CallbackQuery, user: User):
        # most be completed
        text, markup = admin_generate_link()
        self.bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            reply_markup=markup,
            parse_mode='HTML'
        )

    def superuser_handle(self, call: CallbackQuery, user: User):
        text, markup = super_admin_generate_link()
        self.bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            reply_markup=markup,
            parse_mode="HTML"
        )