# completed successfully ✅
from telegram.core.bot.handler import CallbackHandler, CallbackQuery
from telegram.models import TelegramUser as User, Status
from telegram.mods.menu import supperadmin_start
from django.conf import settings
from time import sleep

class ChangeStausCallbackHandler(CallbackHandler):
    def callback_check(self, call: CallbackQuery) -> bool:
        return call.data in ('active', 'inactive')

    def user_handle(self, call: CallbackQuery, user: User):
        pass
    def admin_handle(self, call: CallbackQuery, user: User):
        pass
    def superuser_handle(self, call: CallbackQuery, user: User):

        status, created = Status.objects.get_or_create(defaults={'status': True}, token=settings.TELEGRAM_BOT_TOKEN)

        if call.data == 'active':
            try:
                self.bot.send_chat_action(chat_id=call.message.chat.id, action="typing", timeout=3)
                sleep(3)
                status.status = True
                status.save()
                self.bot.answer_callback_query(callback_query_id=call.id, text=f"Bot Started Successfully!",
                                               show_alert=True)
                text, markup = supperadmin_start(user)
                self.bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=text,
                    reply_markup=markup,
                    parse_mode="HTML",
                )
            except Exception as e:
                self.bot.send_message(
                    chat_id=call.message.chat.id,
                    text=f"Error: {e}",
                )
        else:
            try:
                self.bot.send_chat_action(chat_id=call.message.chat.id, action="typing")
                sleep(3)
                status.status = False
                status.save()
                self.bot.answer_callback_query(callback_query_id=call.id, text=f"Bot Stoped Successfully!",
                                               show_alert=True)
                text, markup = supperadmin_start(user)
                self.bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=text,
                    reply_markup=markup,
                    parse_mode="HTML",
                )
            except Exception as e:
                self.bot.send_message(
                    chat_id=call.message.chat.id,
                    text=f"Error: {e}",
                )