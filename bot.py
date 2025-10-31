import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Load bot token from environment variable for safety
TOKEN = os.getenv("BOT_TOKEN", "8122545395:AAEPRCfDKZquAlgXMcuzLyF78MB9_vU-FJw")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        # Removed the first button
        [InlineKeyboardButton("Play Game", callback_data="play")],
        [InlineKeyboardButton("Visit Ad", url="https://example.com")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Choose an option:", reply_markup=reply_markup)

# Button callback handler
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "play":
        await query.edit_message_text(text="🎮 Game started! Enjoy!")
    else:
        await query.edit_message_text(text=f"Selected option: {query.data}")

# Error handler
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

# Main function
def main():
    # Create the Application and pass it your bot's token.
    app = ApplicationBuilder().token(TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_error_handler(error_handler)

    # Run the bot using polling
    logger.info("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
