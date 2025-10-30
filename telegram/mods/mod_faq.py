from telegram.core.bot.handler import CallbackQuery, CallbackHandler
from telegram.models import TelegramUser as User
from telegram.mods.mod_start import StartHandler


class FAQ(CallbackHandler):
    def callback_check(self, call: CallbackQuery) -> bool:
        return call.data == "faq"

    @property
    def text(self):
        return (
                "💎 Frequently Asked Questions about the Limizer Telegram Bot (Limizer Gold)\n\n"
                "---\n\n"
                "🤖 1. What exactly does the Limizer bot do?\n\n"
                "Limizer Gold is an intelligent analytical assistant on Telegram specifically designed for the global gold market (XAU/USD). "
                "The bot analyzes price behavior, past reactions, and liquidity clusters to identify probable buy and sell areas, and sends alerts 📲 to the user on Telegram. "
                "Unlike pure signal bots, Limizer acts like a 24/7 assisting analyst so you can see precise market reaction zones in real time and make your own decisions based on experience.\n\n"
                "---\n\n"
                "📊 2. Do I need technical analysis knowledge to use Limizer?\n\n"
                "Yes ✅ "
                "A basic familiarity with technical analysis is necessary to use Limizer effectively. "
                "Limizer shows you important price zones, but final interpretation is up to you. "
                "We recommend combining its alerts with support and resistance levels, trend lines, candle behavior, and volume to form a fuller analysis. "
                "Using this approach helps you set more precise entry points, optimized stop loss, and take profit levels, improving the accuracy of your decisions.\n\n"
                "---\n\n"
                "⚙ 3. Does Limizer trade automatically?\n\n"
                "No ❌ "
                "Limizer does not open or close any trades automatically. "
                "Its primary role is market analysis and price-based alerts so the user can decide calmly and without emotion. "
                "In short, Limizer works as an impartial trading advisor — it does not give orders or handle your funds — it only clarifies market conditions.\n\n"
                "---\n\n"
                "⏰ 4. When should I avoid using Limizer alerts?\n\n"
                "There are certain market periods where emotional volatility reduces data reliability. "
                "We recommend avoiding entering trades during the following times 🚫\n\n"
                "- 30 minutes before and 30 minutes after major economic news (e.g., NFP, CPI, FOMC) 📰\n"
                "- The first two hours of the Sydney session 🌏\n"
                "- The first 30 minutes of the New York session 🕒\n\n"
                "During these periods, the market often lacks a clear direction and shows sudden movements. "
                "If you receive a Limizer alert at these times, avoid entering trades and wait for price to stabilize.\n\n"
                "---\n\n"
                "👥 5. Who is Limizer suitable for?\n\n"
                "Limizer is built for all gold traders who seek discipline and professional analysis:\n\n"
                "⚡ Scalpers: who need fast alerts and real-time price reactions.\n"
                "🎯 Day traders: who want precise daily buy/sell zones.\n"
                "💰 Swing traders and investors: who look for more reliable zones for longer-term decisions.\n\n"
                "Limizer is a tool for those who want to guess less and decide more based on real data."
                )


    def user_handle(self, call: CallbackQuery, user: User):
        self.bot.send_message(call.message.chat.id, self.text)
    def admin_handle(self, call: CallbackQuery, user: User):
        pass
    def superuser_handle(self, call: CallbackQuery, user: User):
        pass