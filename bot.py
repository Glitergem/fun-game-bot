import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
import os

# --- CONFIGURATION ---
TOKEN = "8122545395:AAEPRCfDKZquAlgXMcuzLyF78MB9_vU-FJw"

# --- SETUP ---
logging.basicConfig(level=logging.INFO)

# --- START COMMAND ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "👋 សួស្តី! ស្វាគមន៍មកកាន់ **Fun Game Hub** 🎮\n\n"
        "នៅទីនេះអ្នកអាចសាកល្បងហ្គេមសប្បាយៗ និងស្វែងយល់អំពីបូតថ្មីៗ។\n\n"
        "👉 ចុចខាងក្រោមដើម្បីចូលទៅកាន់បូតចម្បង៖"
    )

    keyboard = [[InlineKeyboardButton("👉 ទស្សនាបូតចម្បង 🎯", url="https://t.me/faxkh888888888bot")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)

# --- RUN BOT ---
def main():
    application = Application.builder().token(TOKEN).build()
    
    # Add only start command handler
    application.add_handler(CommandHandler("start", start))
    
    print("🤖 Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()
