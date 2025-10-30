# completed successfully ✅
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from telegram.core.bot.handler import CallbackHandler
from telegram.models import TelegramUser as User
from telegram.utils.generate import generate_one_time_admin_link
from django.utils import timezone

class ViewUsers(CallbackHandler):
    def callback_check(self, call: CallbackQuery) -> bool:
        return call.data == "gl_view_admins"

    def user_handle(self, call: CallbackQuery, user: User):
        # regular user view (not needed here)
        pass

    def admin_handle(self, call: CallbackQuery, user: User):
        pass
    def superuser_handle(self, call: CallbackQuery, user: User):
        """
        Generate a one-time link and send a polished English admin message.
        generate_one_time_link may return either:
          - a link string, or
          - a tuple (link, token_obj) where token_obj may have .token and .expires_at
        """
        try:
            url, token = generate_one_time_admin_link(user)
        except Exception as e:
            # send error to admin
            self.bot.send_message(
                user.chat_id,
                f"❌ Error while generating one-time link:\n`{e}`",
                parse_mode='Markdown'
            )
            return
        token_value = token.token
        expires_text = "Unknown"

        # Build inline keyboard
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("🔗 Open link", url=url))

        # Build HTML message (safe and clear)
        username = user.username
        user_ident = f"{username} (id: {user.chat_id})"
        created_text = ""
        if token is not None:
            created_at = token.created
            if created_at:
                try:
                    created_text = created_at.astimezone(timezone.get_current_timezone()).strftime("%Y-%m-%d %H:%M:%S %Z")
                except Exception:
                    created_text = str(created_at)

        message_html = (
            "<b>✅ One-time access link generated successfully</b>\n\n"
            f"👤 <b>User:</b> <code>{user_ident}</code>\n"
            f"🔗 <b>Link:</b> <a href=\"{url}\">Open link</a>\n"
            f"🆔 <b>Token:</b> <code>{token_value}</code>\n"
            f"⏳ <b>Expires at:</b> <code>10 minutes after creating</code>\n"
        )

        if created_text:
            message_html += f"🕒 <b>Created at:</b> <code>{created_text}</code>\n"
        message_html += "\nUse the button above for direct access."
        self.bot.send_message(
            user.chat_id,
            message_html,
            reply_markup=kb,
            parse_mode='HTML'
        )
