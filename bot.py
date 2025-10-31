from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# ===== CONFIG =====
TOKEN = "8122545395:AAEPRCfDKZquAlgXMcuzLyF78MB9_vU-FJw"  # Your bridge bot token
MAIN_BOT_LINK = "https://t.me/faxkh888888888bot"  # Main finance bot link

# ===== COMMAND HANDLERS =====
def start(update: Update, context: CallbackContext):
    """Send a welcome message with options."""
    keyboard = [
        [InlineKeyboardButton("💡 Learn Finance Tips", callback_data='tips')],
        [InlineKeyboardButton("🔗 Visit Main Bot (Optional)", url=MAIN_BOT_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "Welcome to Finance Helper Bot! 🌟\n\n"
        "Choose what you want to do:\n"
        "1️⃣ Learn tips & tricks about managing your money.\n"
        "2️⃣ Optional: Visit our full Finance Bot for more tools.\n\n"
        "Click a button below to continue.",
        reply_markup=reply_markup
    )

def button(update: Update, context: CallbackContext):
    """Handle button presses inside the bot."""
    query = update.callback_query
    query.answer()

    if query.data == 'tips':
        tips = [
            "💰 Tip 1: Always save at least 10% of your income.",
            "📊 Tip 2: Track your expenses weekly to spot leaks.",
            "🏦 Tip 3: Diversify your savings between short-term & long-term goals.",
            "📈 Tip 4: Avoid high-interest debt whenever possible."
        ]
        for tip in tips:
            query.message.reply_text(tip)
    else:
        query.message.reply_text("Unknown option.")

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text("Use /start to see options.")

# ===== MAIN FUNCTION =====
def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CallbackQueryHandler(button))

    print("Bridge bot is running...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
