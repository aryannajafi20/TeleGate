# completed successfully ✅
from datetime import timedelta
from django.utils import timezone
from telegram.core.bot.handler import Handler, Message
from telegram.models import TelegramUser as User, Invite, Plan
from telegram.mods.menu import user_start, supperadmin_start, admin_start, unknown_starts
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class StartHandler(Handler):
    def check(self, message: Message) -> bool:
        return message.text.startswith('/start')

    def process_invitation(self, message: Message, user: User, token):
        invite = Invite.objects.filter(token=token, receiver__isnull=True)

        if invite.exists():
            invite = invite.last()
            if invite.is_expired:
                self.bot.send_message(chat_id=message.chat.id, text="❌ Invite link has been expired")
                invite.delete()
                return False
            invite.receiver = user
            invite.save()
            user.invited = True
            user.name = invite.name
            user.is_admin = True if invite.role == 'admin' else False
            user.save()
            self.bot.send_message(chat_id=message.chat.id, text="✅ Invite Accepted Successfully")
            return True
        return False
    def process_plan(self, message: Message, user: User, token):
        plan = Plan.objects.filter(token=token, receiver__isnull=True)
        if plan.exists():
            plan = plan.last()
            if plan.is_expired or plan.is_used:
                self.bot.send_message(chat_id=message.chat.id, text="❌ Subscription link has been expired")
                plan.delete()
                return False
            plan.receiver = user
            plan.is_active = True
            plan.activated = timezone.now()
            plan.save()
            user.subscription = True
            user.subscription_date = timezone.now() + timedelta(days=plan.days)
            user.save()
            self.bot.send_message(chat_id=message.chat.id, text="✅ Subscription Activated Successfully")
            return True
        return False
    def user_handle(self, message: Message, user: User):

        if not user.invited:
            data = message.text.split()
            if len(data) != 2:
                text, markup = unknown_starts()
                self.bot.send_message(chat_id=message.chat.id, text=text, parse_mode="HTML", reply_markup=markup)
                return
            if data[1].startswith("inv_"):
                token = data[1][4:]
                if self.process_invitation(message, user, token):
                    self.user_start(message, user)
                    return
                else:
                    return
            else:
                return
        if not user.subscription and len(message.text.split()) == 2:
            data = message.text.split()
            if data[1].startswith("sub_"):
                token = data[1][4:]
                if self.process_plan(message, user, token):
                    self.user_start(message, user)
                    return
                else:
                    return
            else:
                return
        self.user_start(message, user)


    def user_start(self, message: Message, user: User):
        text, markup = user_start()
        self.bot.send_message(
            chat_id=message.chat.id,
            text=text,
            reply_markup=markup,
            parse_mode='HTML'
        )
    def admin_handle(self, message: Message, user: User):
        text, markup = admin_start(user)
        self.bot.send_message(
            chat_id=message.chat.id,
            text=text,
            reply_markup=markup,
            parse_mode='HTML'
        )
    def superuser_handle(self, message: Message, user: User):

        text, markup = supperadmin_start(user)
        self.bot.send_message(
            chat_id=message.chat.id,
            text=text,
            reply_markup=markup,
            parse_mode='HTML'
        )