# completed successfully ✅
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from telegram.core.bot.handler import CallbackHandler, CallbackQuery
from telegram.models import TelegramUser as User, Plan
from django.conf import settings
from time import sleep


class GenerateSubscriptionLinkCallbackHandler(CallbackHandler):
    def callback_check(self, call: CallbackQuery) -> bool:
        return call.data == 'gl_subscription'

    def user_handle(self, call: CallbackQuery, user: User):
        pass

    def admin_handle(self, call: CallbackQuery, user: User):
        self.superuser_handle(call, user)

    def superuser_handle(self, call: CallbackQuery, user: User):
        # Clear prompt with example and cancel option
        msg = self.bot.send_message(
            chat_id=call.message.chat.id,
            text=(
                "🗓️ *Create subscription link*\n\n"
                "Please enter the duration in days (example: `7` or `30`).\n"
                "This link will grant the recipient access for the given number of days *after they activate it*.\n\n"
                "Type `cancel` to abort."
            ),
            parse_mode='Markdown'
        )
        self.bot.register_next_step_handler(msg, self.get_days, user=user)

    def get_days(self, message: Message, user: User):
        text = (message.text or "").strip().lower()
        if text == "cancel":
            self.bot.send_message(chat_id=message.chat.id, text="❎ Operation canceled.")
            return

        if not text.isdigit():
            self.bot.send_message(
                chat_id=message.chat.id,
                text="❌ Invalid input. Please send the number of days as digits (for example `7`).",
            )
            return

        days = int(text)
        if days <= 0:
            self.bot.send_message(
                chat_id=message.chat.id,
                text="❌ Number of days must be greater than zero. Try again or type `cancel`.",
            )
            return

        progress = self.bot.send_message(
            chat_id=message.chat.id,
            text="⚙️ Generating subscription link — please wait..."
        )
        self.bot.send_chat_action(chat_id=message.chat.id, action="typing", timeout=2)
        sleep(2)
        try:
            subs = Plan.objects.create(
                creator=user,
                days=days,
            )

            # Use a clear start payload to avoid collisions with other start handlers
            start_link = f"https://t.me/{settings.TELEGRAM_BOT_USERNAME}?start=sub_{subs.token}"

            # Inline keyboard (kept simple as requested)
            kb = InlineKeyboardMarkup()
            kb.add(InlineKeyboardButton(text="📤 Forward Invite", switch_inline_query=start_link))
            kb.add(InlineKeyboardButton(text="➕ Create Another", callback_data="generate_subs_link"))

            # Friendly final message — explains exact behaviour and next steps
            explanation = (
                "✅ <b>Subscription link created</b>\n\n"
                f"• <b>Duration:</b> {subs.days} day(s)\n"
                "• <b>How it works:</b> The recipient must open the link to activate the subscription. "
                "Once activated, the subscription will be valid for the number of days above.\n\n"
                f"• <b>Token:</b> <code>{subs.token}</code>\n\n"
                "You can forward the start link to the user now. To revoke later, use the admin panel or delete the subscription record."
            )

            # Edit the progress message with the final UX-focused text
            self.bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=progress.message_id,
                text=explanation,
                parse_mode='HTML',
                reply_markup=kb,
            )

        except Exception:
            self.bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=progress.message_id,
                text="❌ An error occurred while creating the subscription. Please try again later."
            )
