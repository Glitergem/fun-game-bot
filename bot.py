# bot.py
import logging
import os
import urllib.request
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ====== CONFIG (hardcoded as requested) ======
# NOTE: keeping token here is insecure for public repos — it's included because you asked.
TOKEN = "8122545395:AAEPRCfDKZquAlgXMcuzLyF78MB9_vU-FJw"
MAIN_BOT_LINK = "https://t.me/faxkh888888888bot"

# If you also use .env locally, this keeps compatibility but won't override the hardcoded token
load_dotenv()
_env_token = os.getenv("BOT_TOKEN")
if _env_token:
    TOKEN = _env_token  # environment variable takes precedence if set

# ====== LOGGING ======
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# ====== UTIL: delete webhook to avoid 409 Conflict ======
def try_delete_webhook(token: str):
    """
    Calls Telegram deleteWebhook before starting polling to avoid 'terminated by other getUpdates request' conflicts.
    This is a simple HTTP call and will not raise if it fails.
    """
    url = f"https://api.telegram.org/bot{token}/deleteWebhook"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            logger.info("Called deleteWebhook: %s", resp.read(200))
    except Exception as e:
        logger.warning("Could not call deleteWebhook (non-fatal): %s", e)


# ====== HANDLERS ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔗 ចូលទៅបូតដើម (ចុចទីនេះ)", url=MAIN_BOT_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Use message if available; safe guard if invoked in other contexts
    if update.message:
        await update.message.reply_text(
            "សួស្តី! 👋\n\n"
            "សូមចុចខាងក្រោម ដើម្បីចូលទៅកាន់បូតដើម 🌟\n\n"
            "👇 ចុចទីនេះ 👇",
            reply_markup=reply_markup,
        )
    else:
        # fallback
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="សូមចុចខាងក្រោម ដើម្បីចូលទៅកាន់បូតដើម:",
            reply_markup=reply_markup,
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🆘 ជំនួយ\n\n"
        "ចុចប៊ូតុងខាងក្រោម ដើម្បីចូលទៅកាន់បូតដើម:\n"
        f"{MAIN_BOT_LINK}"
    )


# ====== MAIN ======
def main():
    # Ensure token is present
    if not TOKEN:
        logger.error("BOT token is empty. Exiting.")
        raise SystemExit("BOT token is empty. Set BOT_TOKEN or hardcode TOKEN in the script.")

    # Try deleting any existing webhook to avoid getUpdates 409 conflict
    try_delete_webhook(TOKEN)

    # Build application
    app = ApplicationBuilder().token(TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    logger.info("🤖 Promo bot is starting (polling).")
    # Run using polling
    app.run_polling()


if __name__ == "__main__":
    main()
