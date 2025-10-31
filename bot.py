import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# === CONFIG ===
TOKEN = "8219450701:AAF4CKj5ihdN5kAztEhZQVIFPO04MLII_Hs"  # Your bot token
MAIN_BOT_LINK = "https://t.me/faxkh888888888bot"

# === FINANCE TIPS ===
FINANCE_TIPS = [
    "💡 គន្លឹះទី១៖ ចាប់ផ្តើមរក្សាសន្សំ ១០% នៃប្រាក់ចំណូលរាល់ខែ។",
    "💡 គន្លឹះទី២៖ កុំខ្ចីលុយដើម្បីទិញអ្វីដែលមិនចាំបាច់។",
    "💡 គន្លឹះទី៣៖ បង្កើនចំណេះដឹងហិរញ្ញវត្ថុជារៀងរាល់ថ្ងៃ។",
    "💡 គន្លឹះទី៤៖ ចំណាយតិចជាងប្រាក់ចំណូលរបស់អ្នក។",
    "💡 គន្លឹះទី៥៖ វិនិយោគលើការអប់រំ និងជំនាញរបស់អ្នក។",
]

first_time_users = set()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- START COMMAND ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💡 យល់ដឹងអំពីហិរញ្ញវត្ថុ", callback_data="tips")],
        [InlineKeyboardButton("🔗 ចូលទៅបូតដើម (ជាជម្រើស)", url=MAIN_BOT_LINK)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "សួស្តី! 👋\n\n"
        "បូតរៀនហិរញ្ញវត្ថុ 🌟\n"
        "ស្វែងយល់ពីចំណេះដឹង និងបច្ចេកទេសគ្រប់គ្រងលុយ។\n\n"
        "ជ្រើសរើសជម្រើសខាងក្រោម៖",
        reply_markup=reply_markup,
    )

# --- HELP COMMAND ---
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🆘 ជំនួយ\n\n"
        "💡 យល់ដឹងអំពីហិរញ្ញវត្ថុ → ទទួលបានគន្លឹះគ្រប់គ្រងលុយ\n"
        "🔗 ចូលទៅបូតដើម → ទៅកាន់បូតដើមសម្រាប់មុខងារបន្ថែម\n\n"
        "សូមចុច /start ដើម្បីចាប់ផ្តើមឡើងវិញ 🌟"
    )

# --- BUTTON HANDLER ---
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return
    await query.answer()

    user_id = query.from_user.id

    if query.data == "tips":
        if user_id not in first_time_users:
            await query.message.reply_text("💡 សូមស្វាគមន៍! នេះជាគន្លឹះហិរញ្ញវត្ថុថ្មីៗរបស់អ្នក។")
            first_time_users.add(user_id)

        for tip in FINANCE_TIPS:
            await query.message.reply_text(tip)

        keyboard = [[InlineKeyboardButton("⬅️ ត្រឡប់ទៅមុខម៉ឺនុយ", callback_data="back")]]
        await query.message.reply_text(
            "ជ្រើសរើសសកម្មភាពបន្ទាប់៖",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "back":
        keyboard = [
            [InlineKeyboardButton("💡 យល់ដឹងអំពីហិរញ្ញវត្ថុ", callback_data="tips")],
            [InlineKeyboardButton("🔗 ចូលទៅបូតដើម (ជាជម្រើស)", url=MAIN_BOT_LINK)],
        ]
        await query.message.reply_text(
            "ត្រឡប់មកម៉ឺនុយដើមវិញ 🌟\nសូមជ្រើសរើសជម្រើសថ្មី៖",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

# --- MAIN FUNCTION ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button))
    logger.info("🤖 Learning Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
