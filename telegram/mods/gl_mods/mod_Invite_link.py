# completed successfully ✅
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from telegram.core.bot.handler import CallbackHandler, CallbackQuery
from telegram.models import TelegramUser as User, Invite
from django.conf import settings
from time import sleep



class GenerateInviteLinkCallbackHandler(CallbackHandler):
    def callback_check(self, call: CallbackQuery) -> bool:
        return call.data == "gl_invite"

    def user_handle(self, call: CallbackQuery, user: User):
        pass

    def admin_handle(self, call: CallbackQuery, user: User):
        self.superuser_handle(call, user)

    def superuser_handle(self, call: CallbackQuery, user: User):
        msg = self.bot.send_message(
            chat_id=call.message.chat.id,
            text="📝 Please enter a name for this invite:",
        )
        self.bot.register_next_step_handler(msg, self.get_name, user=user)

    def get_name(self, message: Message, user: User):
        name = (message.text or "").strip()
        if not name:
            self.bot.send_message(
                chat_id=message.chat.id,
                text="⚠️ Name cannot be empty. Please try again."
            )
            return

        progress = self.bot.send_message(
            chat_id=message.chat.id,
            text="⚙️ Generating invite link, please wait..."
        )
        self.bot.send_chat_action(chat_id=message.chat.id, action="typing", timeout=2)
        sleep(2)

        try:
            invite = Invite.objects.create(
                creator=user,
                name=name,
                role='user'
            )

            # ✅ Create Telegram start link for this invite
            start_link = f"https://t.me/{settings.TELEGRAM_BOT_USERNAME}?start=inv_{invite.token}"


            kb = InlineKeyboardMarkup()
            kb.add(InlineKeyboardButton(text="📤 Forward Invite", switch_inline_query=start_link))
            kb.add(InlineKeyboardButton(text="➕ Create Another", callback_data="gl_invite"))

            # Edit message with final info
            self.bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=progress.message_id,
                text=(
                    f"✅ Invite link created successfully!\n\n"
                    f"🔰 Name: <b>{invite.name}</b>\n"
                    f"🆔 Token: <code>{invite.token}</code>\n\n"
                    f"📎 Link:\n<code>{start_link}</code>\n\n"
                ),
                parse_mode='HTML',
                reply_markup=kb,
            )

        except Exception as e:
            self.bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=progress.message_id,
                text="❌ An error occurred while creating the invite. Please try again later."
            )