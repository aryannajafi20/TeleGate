# completed successfully ✅
from telegram.core.bot.handler import CallbackHandler, CallbackQuery
from telegram.models import TelegramUser as User


class EnableAlertsCallbackHandler(CallbackHandler):
    def callback_check(self, call: CallbackQuery) -> bool:
        return call.data == 'enable_alerts'

    def user_handle(self, call: CallbackQuery, user: User):
        self.superuser_handle(call, user)

    def admin_handle(self, call: CallbackQuery, user: User):
        self.superuser_handle(call, user)

    def superuser_handle(self, call: CallbackQuery, user: User):
        try:
            user.has_permission = True
            user.save()
            self.bot.answer_callback_query(
                callback_query_id=call.id,
                text=f'✅ Alerts have been successfully enabled!',
                show_alert=False,
                cache_time=3
            )
        except Exception:
            self.bot.answer_callback_query(
                call.id,
                text="❌ Something went wrong. Please try again.",
                show_alert=True
            )
class DisableAlertsCallbackHandler(CallbackHandler):
    def callback_check(self, call: CallbackQuery) -> bool:
        return call.data == 'disable_alerts'

    def user_handle(self, call: CallbackQuery, user: User):
        self.superuser_handle(call, user)

    def admin_handle(self, call: CallbackQuery, user: User):
        self.superuser_handle(call, user)


    def superuser_handle(self, call: CallbackQuery, user: User):
        try:
            user.has_permission = False
            user.save()
            self.bot.answer_callback_query(
                callback_query_id=call.id,
                text=f'✅ Alerts have been successfully disabled.',
                show_alert=False,
                cache_time=3
            )
        except Exception:
            self.bot.answer_callback_query(
                call.id,
                text="❌ Something went wrong. Please try again.",
                show_alert=True
            )