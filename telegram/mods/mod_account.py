# completed successfully ✅
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telegram.core.bot.handler import CallbackHandler
from telegram.models import TelegramUser as User
from django.utils import timezone

class AccountHandler(CallbackHandler):
    """
    Shows a neat account card for the current user with quick actions.
    Buttons:
      - Edit Profile (callback: edit_account)
      - Copy ID (callback: copy_user_id:<chat_id>)  <-- implement the callback to send the plain ID
      - Back (callback: back_to_menu)
      - Support (opens support link)
    """
    def callback_check(self, call: CallbackQuery) -> bool:
        return call.data == "account"

    def user_handle(self, call: CallbackQuery, user: User):
        # Safe extraction of fields with fallbacks
        display_name = user.name or user.username
        username = user.username
        chat_id = user.chat_id
        is_active = user.subscription
        # created/joined date (best-effort)
        created_at = user.created
        if created_at:
            try:
                created_text = created_at.astimezone(timezone.get_current_timezone()).strftime("%Y-%m-%d %H:%M:%S %Z")
            except Exception:
                created_text = str(created_at)
        else:
            created_text = "Unknown"

        # Build the message (HTML)
        message_text = (
            f"👤 <b>Account</b>\n"
            f"• <b>Name:</b> {display_name}\n"
            + (f"• <b>Username:</b> @{username}\n" if username else "")
            + f"• <b>Chat ID:</b> <code>{chat_id}</code>\n"
            f"• <b>Subscription:</b> {'Active' if is_active else 'Inactive'}\n"
            f"• <b>Role:</b> {'User'}\n"
            f"• <b>Joined:</b> {created_text}\n\n"
        )

        kb = InlineKeyboardMarkup()
        kb.row(
            InlineKeyboardButton("◀️ Back", callback_data="back_to_start_menu")
        )

        # Send or edit message: prefer editing the current message if it exists
        try:
            # If the callback came from an inline message, edit it; otherwise send a new message
            if call.message:
                # edit the message that had the inline keyboard
                self.bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=message_text,
                    parse_mode="HTML",
                    reply_markup=kb
                )
            else:
                self.bot.send_message(
                    call.from_user.id,
                    message_text,
                    parse_mode="HTML",
                    reply_markup=kb
                )
        except Exception:
            # fallback to sending a new message if edit fails
            self.bot.send_message(
                call.from_user.id,
                message_text,
                parse_mode="HTML",
                reply_markup=kb
            )

    def admin_handle(self, call: CallbackQuery, user: User):
        # Safe extraction of fields with fallbacks
        display_name = user.name or user.username or "Unknown"
        username = user.username or "Unknown"
        chat_id = user.chat_id
        is_active = user.is_active
        is_admin = True
        # created/joined date (best-effort)
        created_at = user.created
        if created_at:
            try:
                created_text = created_at.astimezone(timezone.get_current_timezone()).strftime("%Y-%m-%d %H:%M:%S %Z")
            except Exception:
                created_text = str(created_at)
        else:
            created_text = "Unknown"

        # Build the message (HTML)
        message_text = (
            f"👤 <b>Account</b>\n"
            f"• <b>Name:</b> {display_name}\n"
            + (f"• <b>Username:</b> @{username}\n" if username else "")
            + f"• <b>Chat ID:</b> <code>{chat_id}</code>\n"
            f"• <b>Status:</b> {'Active' if is_active else 'Inactive'}\n"
            f"• <b>Role:</b> {'Admin' if is_admin else 'User'}\n"
            f"• <b>Joined:</b> {created_text}\n\n"
        )

        kb = InlineKeyboardMarkup()
        kb.row(
            InlineKeyboardButton("◀️ Back", callback_data="back_to_start_menu")
        )

        # Send or edit message: prefer editing the current message if it exists
        try:
            # If the callback came from an inline message, edit it; otherwise send a new message
            if call.message:
                # edit the message that had the inline keyboard
                self.bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=message_text,
                    parse_mode="HTML",
                    reply_markup=kb
                )
            else:
                self.bot.send_message(
                    call.from_user.id,
                    message_text,
                    parse_mode="HTML",
                    reply_markup=kb
                )
        except Exception:
            # fallback to sending a new message if edit fails
            self.bot.send_message(
                call.from_user.id,
                message_text,
                parse_mode="HTML",
                reply_markup=kb
            )


    def superuser_handle(self, call: CallbackQuery, user: User):
        # Safe extraction of fields with fallbacks
        display_name = user.name or user.username or "Unknown"
        username = user.username
        chat_id = user.chat_id
        is_active = user.is_superuser or user.is_active
        is_admin = user.is_superuser
        # created/joined date (best-effort)
        created_at = user.created
        if created_at:
            try:
                created_text = created_at.astimezone(timezone.get_current_timezone()).strftime("%Y-%m-%d %H:%M:%S %Z")
            except Exception:
                created_text = str(created_at)
        else:
            created_text = "Unknown"

        # Build the message (HTML)
        message_text = (
            f"👤 <b>Account</b>\n"
            f"• <b>Name:</b> {display_name}\n"
            + (f"• <b>Username:</b> @{username}\n" if username else "")
            + f"• <b>User ID:</b> <code>{chat_id}</code>\n"
            f"• <b>Status:</b> {'Active' if is_active else 'Inactive'}\n"
            f"• <b>Role:</b> Super Admin\n"
            f"• <b>Joined:</b> {created_text}\n\n"
        )

        kb = InlineKeyboardMarkup()
        kb.row(
            InlineKeyboardButton("◀️ Back", callback_data="back_to_start_menu")
        )

        # Send or edit message: prefer editing the current message if it exists
        try:
            # If the callback came from an inline message, edit it; otherwise send a new message
            if call.message:
                # edit the message that had the inline keyboard
                self.bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=message_text,
                    parse_mode="HTML",
                    reply_markup=kb
                )
            else:
                self.bot.send_message(
                    call.from_user.id,
                    message_text,
                    parse_mode="HTML",
                    reply_markup=kb
                )
        except Exception:
            # fallback to sending a new message if edit fails
            self.bot.send_message(
                call.from_user.id,
                message_text,
                parse_mode="HTML",
                reply_markup=kb
            )



