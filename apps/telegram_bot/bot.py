import os
import asyncio
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# This will be your Mini App HTTPS link - we will get it in Part 4
# For now we use placeholder, you will change it later
WEB_APP_URL = os.getenv("WEB_APP_URL", "https://your-vercel-link.vercel.app")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🚀 Open Grandmaster OS", web_app=WebAppInfo(url=WEB_APP_URL))],
        [InlineKeyboardButton("📋 View Task Board", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Welcome to Grandmaster OS!\n\n"
        "I am your AI company. Tap below to open the Mini App:\n"
        "• Create Tasks\n"
        "• Assign to Agents\n"
        "• Review GitHub PR\n"
        "• Approve Vercel Deploy",
        reply_markup=reply_markup
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use /start to open the Mini App.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    print("Bot is running... Go to Telegram and send /start")
    app.run_polling()

if __name__ == "__main__":
    main()