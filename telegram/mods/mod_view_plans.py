from telegram.core.bot.handler import CallbackHandler, CallbackQuery
from telegram.models import TelegramUser as User

from telegram.mods.menu import view_plans


class ViewPlansCallbackHandler(CallbackHandler):
    def callback_check(self, call: CallbackQuery) -> bool:
        return call.data == 'view_plans'

    def user_handle(self, call: CallbackQuery, user: User):
        text, markup = view_plans()
        self.bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            parse_mode="HTML",
            reply_markup=markup
        )
        return
    def admin_handle(self, call: CallbackQuery, user: User):
        pass
    def superuser_handle(self, call: CallbackQuery, user: User):
        pass