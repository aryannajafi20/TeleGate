# 🧩 TeleGate Installation Guide

Welcome to **TeleGate** — a Telegram user management system built with **Django**, **TeleBot**, and **SQLite**.

This guide will help you set up the project step by step.

---

## 🪄 Step 1 — Clone the Repository

Clone the repository from GitHub using the following commands:

```bash
git clone https://github.com/your-username/telegate.git
cd telegate
```
___
## ⚙️ Step 2 — Configure Environment Variables
After cloning, open the  `.env` file located in the root directory.
This file contains sensitive configuration values used by Django and the Telegram bot.

Example .env file:

```bash
SECRET_KEY=your-own-secret-key
DEBUG=True
ALLOWED_HOSTS=*
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_BOT_USERNAME=your-telegram-bot-username
SITE_URL=https://your-domain.com
```
___
## 📘 Explanation:

- SECRET_KEY → Used by Django for security (generate your own key).

- DEBUG → Keep True for development; use False in production.

- ALLOWED_HOSTS → Add your domain or IP (e.g., 127.0.0.1 or example.com).

- TELEGRAM_BOT_TOKEN → Your bot’s token from @BotFather

- SUPPORT_USERNAME → your telegram username

- TELEGRAM_BOT_USERNAME → Your bot’s username.

- SITE_URL → Base URL of your website or backend API.

### ⚠️ Important Notes:

- Never commit .env files to GitHub.

- Keep your SECRET_KEY and TELEGRAM_BOT_TOKEN private.

- Double-check spelling before saving.

___

## 🧰 Step 3 — Create a Virtual Environment

To keep project dependencies isolated, create a virtual environment:

```bash
python -m venv env
```

Activate it:

- on **Windows**:
```bash
env\Scripts\activate
```
- on **Linux**:
```bash
source env/bin/activate
```
📘 You’ll see `(venv)` appear before your terminal prompt — that means it’s active.

___

## 📦 Step 4 — Install Dependencies

Install all the required libraries listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```
📘 This installs Django, TeleBot, and all other dependencies your project needs.

___

## 🗄️ Step 5 — Run Database Migrations

Initialize the database by applying Django migrations:
```bash
python manage.py migrate
```

📘 This command creates all the necessary tables in your SQLite database.

___

## 🧑‍💻 Step 6 — Create a Superuser

create a superuser account:
```bash
python manage.py createsuperuser
```

📘 You’ll be prompted to enter your username, email, and password.

___

## ⚡ Step 7 — Run the Django Server

Start the Django backend server:

```bash
python manage.py runserver
```



📘 If everything is correct, you’ll see a message like:


```bash
Starting development server at http://127.0.0.1:8000/
```



Now open your browser and go to:

```bash
http://127.0.0.1:8000/
```

___

## 🤖 Step 8 — Run the Telegram Bot

Make sure your `.env` file is configured correctly (especially the bot token).
Then run the bot:

```bash
python manage.py run
```

📘 Your bot will connect to Telegram and start handling /start commands.

🧠 **How it works**:

- Send `/start` to bot.

- The bot ignores you, and that’s normal.

- Go to django admin panel at `http://127.0.0.1:8000/admin/` and log in.
- Go to **Telegram Users**, select your account, and make yourself a super admin.
- Then send `/start` to the bot again — it should now respond correctly.
