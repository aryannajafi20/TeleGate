from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telegram.models import Status, TelegramUser as User, TelegramUser, Invite
from django.conf import settings
import random

def user_start():
    text = (
                "⚡ Welcome! Your invitation has been accepted.\n\n"
                "Use the buttons below to enable alerts or share this invite with others."
            ),
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("🔔 Enable Alerts", callback_data="enable_alerts"),
        InlineKeyboardButton("🔕 Disable Alerts", callback_data="disable_alerts")
    )

    markup.add(

        InlineKeyboardButton("👤 account", callback_data="account"),
        InlineKeyboardButton("💬 Support", url=f"https://t.me/{settings.SUPPORT_USERNAME}")
    )
    return text, markup


def supperadmin_start(superadmin: User):
    total_users = TelegramUser.objects.filter(is_superuser=False, is_admin=False).count()
    total_active_users = TelegramUser.objects.filter(is_superuser=False, is_admin=False, subscription=True).count()
    total_admins = TelegramUser.objects.filter(is_superuser=False, is_admin=True).count()
    text = (
        f"🧠 <b>Welcome, Super Admin {superadmin.name or superadmin.username}!</b>\n\n"
        f"👥 Total users: {total_users}\n"
        f"🛡️ Admins: {total_admins}\n"
        f"🧩 Permissions: Full Access\n\n"
        "⚙️ <i>You can manage admins, reset systems, and view analytics here.</i>"
    )

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("🔔 Enable Alerts", callback_data="enable_alerts"),
        InlineKeyboardButton("🔕 Disable Alerts", callback_data="disable_alerts")
    )
    markup.row(
        InlineKeyboardButton("👤 account", callback_data="account"),
        InlineKeyboardButton("💬 Support", url=f"https://t.me/{settings.SUPPORT_USERNAME}")

    )
    markup.row(
        InlineKeyboardButton("🔗 Generate Link", callback_data="generate_link")
    )
    status, created = Status.objects.get_or_create(defaults={'status': True}, token=settings.TELEGRAM_BOT_TOKEN)
    if status.status:
        markup.row(
            InlineKeyboardButton("🔴 🛑 Emergency Shutdown (turn bot OFF)", callback_data="inactive")
        )
    else:
        markup.row(
            InlineKeyboardButton("🟢 🚨 Engage System (turn bot ON)", callback_data="active")
        )
    return text, markup


def super_admin_generate_link():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("🔗 Invite Link", callback_data="gl_invite"),
        InlineKeyboardButton("🔗 Admin Link", callback_data="gl_admin"),
    )
    markup.add(
        InlineKeyboardButton("🔗 Subscription Link", callback_data="gl_subscription"),
    )
    markup.row(
        InlineKeyboardButton("🔗 Users List", callback_data="gl_view_users"),
        InlineKeyboardButton("🔗 Admins List", callback_data="gl_view_admins"),

    )
    markup.add(
        InlineKeyboardButton("◀️ Back", callback_data="back_to_start_menu")
    )
    text_en = (
        "🔧 Admin — Invite & Management\n\n"
        "Use the buttons below to manage invites and users:\n\n"
        "🔗 <b>Invite Link</b>\n"
        "Create a Telegram start link for a user — copy it, forward it, or open it directly.\n\n"
        "🔗 <b>Subscription Link</b>\n"
        "Generate a subscription access link (trial or paid) for a user or group.\n\n"
        "🔗 <b>Users List</b>\n"
        "Open a page or link showing all registered users and their status (view/export).\n\n"
        "◀️ <b>Back</b>\n"
        "Return to the main menu."
    )

    return text_en, markup


def admin_start(admin: User):
    active_users = Invite.objects.filter(creator=admin, receiver__isnull=False).count()
    quotes = [
        "“Discipline equals freedom.” – Jocko Willink",
        "“Small steps every day lead to big results.”",
        "“Good leaders inspire others to lead.”",
        "“Success is the sum of small efforts repeated daily.”",
        "“Your future is created by what you do today, not tomorrow.”",
        "“Don’t wish it were easier, wish you were better.” – Jim Rohn",
        "“If you want to change the world, start by making your bed.” – William H. McRaven",
        "“Courage is grace under pressure.” – Ernest Hemingway",
        "“Do something today that your future self will thank you for.”",
        "“Consistency is harder when no one is clapping for you. Keep going anyway.”",
        "“Action is the foundational key to all success.” – Pablo Picasso",
        "“Don’t count the days; make the days count.” – Muhammad Ali",
        "“If it’s important to you, you’ll find a way.”",
        "“Great things never come from comfort zones.”",
        "“The secret of your future is hidden in your daily routine.” – Mike Murdock",
        "“You don’t find willpower; you create it.”",
        "“Discipline is doing what needs to be done even when you don’t feel like it.”",
        "“Push yourself, because no one else is going to do it for you.”",
        "“The pain of discipline is nothing compared to the pain of regret.”",
        "“Every accomplishment starts with the decision to try.”",
        "“Motivation gets you started; discipline keeps you going.”",
        "“Leaders don’t create followers, they create more leaders.” – Tom Peters",
        "“Success is not for the lazy.”",
        "“Be so disciplined that people think you’re obsessed.”",
        "“Fall seven times, stand up eight.” – Japanese Proverb",
        "“Don’t limit your challenges, challenge your limits.”",
        "“If you get tired, learn to rest, not to quit.”",
        "“You don’t have to be extreme, just consistent.”",
        "“The harder you work, the luckier you get.” – Gary Player",
        "“Focus on progress, not perfection.”",
        "“Stay patient and trust your journey.”",
        "“You’ll never always be motivated, so you must learn to be disciplined.”",
        "“Do what is right, not what is easy.”",
        "“Excuses make today easy and tomorrow hard.”",
        "“Dream big. Work hard. Stay humble.”",
        "“Leaders eat last.” – Simon Sinek",
        "“Self-discipline is the best form of self-love.”",
        "“You become unstoppable when you are disciplined.”",
        "“Don’t talk about it. Be about it.”",
        "“If you can’t handle stress, you can’t handle success.”",
        "“Be stronger than your excuses.”",
        "“Results happen over time, not overnight.”",
        "“Do it scared. Do it tired. But do it.”",
        "“Your habits will determine your future.” – Jack Canfield",
        "“Show up even when you don’t feel like it.”",
        "“Success is built on the foundation of discipline.”",
        "“A goal without discipline is just a wish.”",
        "“The man who moves a mountain begins by carrying small stones.” – Confucius",
        "“Winners are made in the dark.”",
        "“Every day you delay is another day you’ll regret later.”",
        "“Be obsessed with improvement.”",
        "“Don’t be afraid to be a beginner.”",
        "“Discipline is choosing between what you want now and what you want most.” – Abraham Lincoln",
        "“Nothing works unless you do.” – Maya Angelou",
        "“Be the kind of leader you would follow.”",
        "“Grind in silence, let success make the noise.”",
        "“The price of discipline is always less than the cost of regret.”",
        "“Success is doing ordinary things extraordinarily well.” – Jim Rohn",
        "“Leadership is practiced not in words but in attitude and action.”",
        "“Work hard in silence, let your success be your voice.”",
        "“You won’t always love the process, but trust it.”",
        "“Losers make excuses. Winners make progress.”",
        "“Your comfort zone is killing your potential.”",
        "“Discipline is the difference between good and great.”",
        "“Leaders are learners.”",
        "“Every expert was once a beginner.”",
        "“Don’t let yesterday take up too much of today.” – Will Rogers",
        "“Success is nothing more than a few simple disciplines practiced every day.”",
        "“Growth begins at the end of your comfort zone.”",
        "“Stay consistent. You’ll thank yourself later.”",
        "“The standard you walk past is the standard you accept.”",
        "“Discipline is destiny.” – Ryan Holiday",
        "“What you do every day matters more than what you do once in a while.”",
        "“A true leader stands firm even when no one follows.”",
        "“Success is not an act but a habit.” – Aristotle",
        "“Leaders don’t wait for opportunities. They create them.”",
        "“Show discipline when no one is watching.”",
        "“Your mindset determines your success.”",
        "“You don’t rise to the level of your goals; you fall to the level of your discipline.” – James Clear",
        "“Don’t wish for it. Work for it.”",
        "“The harder the battle, the stronger the warrior.”",
        "“Be addicted to bettering yourself.”",
        "“Without commitment, you’ll never start. Without consistency, you’ll never finish.” – Denzel Washington",
        "“Discipline is the key that unlocks potential.”",
        "“Start where you are. Use what you have. Do what you can.” – Arthur Ashe",
        "“No one cares, work harder.”",
        "“Leadership is action, not position.” – Donald H. McGannon",
        "“Be the hardest worker in the room.” – Dwayne Johnson",
        "“Don’t let motivation fade; let discipline take over.”",
        "“If you want respect, earn it.”",
        "“Comfort is the enemy of achievement.”",
        "“A lion doesn’t concern himself with the opinion of sheep.”",
        "“Discipline turns dreams into reality.”",
        "“There is no growth without discomfort.”",
        "“You are what you repeatedly do.” – Aristotle",
        "“Success demands sacrifice.”",
        "“Keep moving forward no matter how slow.”",
        "“Hard work beats talent when talent doesn’t work hard.”",
        "“Discipline is remembering what you want.”",
        "“Every day is a chance to improve.”",
        "“Stay hungry. Stay humble.”",
        "“Your only limit is your mind.”"
    ]

    text = (
        f"👑 <b>Welcome back, {admin.name or admin.username}!</b>\n\n"
        f"🧑‍💻 Active users: {active_users}\n"
        f"💬 <i>{random.choice(quotes)}</i>"
    )

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("🔔 Enable Alerts", callback_data="enable_alerts"),
        InlineKeyboardButton("🔕 Disable Alerts", callback_data="disable_alerts")
    )
    markup.row(
        InlineKeyboardButton("👤 account", callback_data="account"),
        InlineKeyboardButton("💬 Support", url=f"https://t.me/{settings.SUPPORT_USERNAME}")

    )
    markup.row(
        InlineKeyboardButton("🔗 Generate Link", callback_data="generate_link")
    )
    return text, markup

def admin_generate_link():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("🔗 Invite Link", callback_data="gl_invite"),
        InlineKeyboardButton("🔗 Users List", callback_data="gl_view_users"),
    )
    markup.row(
        InlineKeyboardButton("🔗 Subscription Link", callback_data="gl_subscription"),
    )
    markup.add(
        InlineKeyboardButton("◀️ Back", callback_data="back_to_start_menu")
    )
    text_en = (
        "🔧 Admin — Invite & Management\n\n"
        "Use the buttons below to manage invites and users:\n\n"
        "🔗 <b>Invite Link</b>\n"
        "Create a Telegram start link for a user — copy it, forward it, or open it directly.\n\n"
        "🔗 <b>Subscription Link</b>\n"
        "Generate a subscription access link (trial or paid) for a user or group.\n\n"
        "🔗 <b>Users List</b>\n"
        "Open a page or link showing all registered users and their status (view/export).\n\n"
        "◀️ <b>Back</b>\n"
        "Return to the main menu."
    )

    return text_en, markup

