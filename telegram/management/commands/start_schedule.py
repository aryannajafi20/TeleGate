import logging
from django.db import transaction
from django.core.management.base import BaseCommand
from apscheduler.schedulers.blocking import BlockingScheduler
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.models import TelegramUser as User, Plan
from telegram.core.bot.bot import bot

logger = logging.getLogger(__name__)

def markup():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🏷️ get subscription", url="https://t.me/limizer_support")
    )
    return kb

class Command(BaseCommand):
    help = "Schedule job that checks expired plans and notifies users."

    def handle(self, *args, **options):
        try:
            bs = BlockingScheduler()
            # اجرا هر 10 دقیقه — مقدار را طبق نیاز خود تغییر بده
            bs.add_job(self.job, 'cron', minute="*/10", id="check_plan_expiry")
            logger.info("Starting scheduler for plan expiry checks.")
            bs.start()
        except Exception as e:
            logger.exception("Scheduler failed to start: %s", e)

    def job(self):
        try:
            # select_related تا از N+1 جلوگیری بشه
            plans_qs = Plan.objects.filter(is_active=True, is_used=False).select_related("receiver")
        except Exception as e:
            logger.exception("Failed to fetch plans: %s", e)
            return

        expired_plan_ids = []
        expired_receiver_ids = []
        notifications = []  # (chat_id, plan_token)

        # نیازی به plans.exists() نیست — اگر خالی باشه حلقه اجرا نمیشه
        for plan in plans_qs.iterator():
            receiver = getattr(plan, "receiver", None)
            if receiver is None:
                # در صورتی که رسیور نداشته باشه، دیتابیس رو تمیز کن (یا فقط لاگ کن)
                logger.warning("Plan %s has no receiver — marking inactive/used.", plan.pk)
                expired_plan_ids.append(plan.pk)
                continue

            try:
                if plan.has_expired:
                    expired_plan_ids.append(plan.pk)
                    expired_receiver_ids.append(receiver.pk)
                    chat_id = getattr(receiver, "chat_id", None)
                    if chat_id:
                        notifications.append((chat_id, plan.token))
                    else:
                        logger.warning("Receiver %s for plan %s has no chat_id.", receiver.pk, plan.pk)
            except Exception as e:
                logger.exception("Error checking expiry for Plan %s: %s", plan.pk, e)
                # در صورت بروز خطا برای این پلان، از پردازش آن عبور کن
                continue

        if not expired_plan_ids:
            logger.debug("No expired plans found in this run.")
            return

        # انجام تغییرات در دیتابیس به صورت bulk داخل تراکنش
        try:
            with transaction.atomic():
                Plan.objects.filter(pk__in=expired_plan_ids).update(is_active=False, is_used=True)
                User.objects.filter(pk__in=expired_receiver_ids).update(subscription=False)
            logger.info("Marked %d plans expired and %d users subscription=False.",
                        len(expired_plan_ids), len(expired_receiver_ids))
        except Exception as e:
            logger.exception("Failed to update DB for expired plans/users: %s", e)
            # اگر آپدیت دیتابیس شکست خورد، بهتره ارسال پیام انجام نشه
            return

        # ارسال پیام‌ها پس از آپدیت دیتابیس — هر ارسال را در try/except بپیچ
        for chat_id, plan_token in notifications:
            try:
                bot.send_message(
                    chat_id=chat_id,
                    text=(
                        "⏳ Your subscription has ended.\n\n"
                        "To continue receiving premium signals and updates, please renew your subscription."
                    ),
                    reply_markup=markup(),
                    parse_mode="HTML",
                )
                logger.debug("Sent expiry message to chat_id %s", chat_id)
            except Exception as e:
                logger.exception("Failed to send expiry message to chat_id %s: %s", chat_id, e)
