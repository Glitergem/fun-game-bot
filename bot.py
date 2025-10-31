from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    JobQueue
)
import datetime
import logging

# ===== CONFIG =====
TOKEN = "8122545395:AAEPRCfDKZquAlgXMcuzLyF78MB9_vU-FJw"
MAIN_BOT_LINK = "https://t.me/faxkh888888888bot"

# ===== LOGGING =====
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ===== DATA =====
FINANCE_TIPS = [
    "💰 គន្លឹះ ១: តែងតែសន្សំពេលអតិថិជន ១០% នៃចំណូលរបស់អ្នក។",
    "📊 គន្លឹះ ២: តាមដានចំណាយប្រចាំសប្តាហ៍ដើម្បីរកកន្លែងចំណាយចេញមិនចាំបាច់។",
    "🏦 គន្លឹះ ៣: ចែកចាយការសន្សំរបស់អ្នករវាងគោលបំណងខ្លី និងវែង។",
    "📈 គន្លឹះ ៤: គួរជៀសវាងបំណុលដែលមានការប្រាក់ខ្ពស់។",
    "💡 គន្លឹះ ៥: សិក្សាពីវិធីវិនិយោគតូចៗ ដើម្បីបង្កើនចំណូលបន្ថែម។"
]

# Track first-time users
first_time_users = set()

# ===== COMMAND HANDLERS =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ផ្ញើសារ​ស្វាគមន៍ជាមួយជម្រើស"""
    keyboard = [
        [InlineKeyboardButton("💡 យល់ដឹងអំពីហិរញ្ញវត្ថុ", callback_data='tips')],
        [InlineKeyboardButton("🔗 ចូលទៅបូតដើម (ជាជម្រើស)", url=MAIN_BOT_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "ស្វាគមន៍មកកាន់បូតជំនួយហិរញ្ញវត្ថុ! 🌟\n\n"
        "សូមជ្រើសរើសអ្វីដែលអ្នកចង់ធ្វើ៖\n"
        "1️⃣ យល់ដឹងអំពីចំណេះដឹង និងបច្ចេកទេសគ្រប់គ្រងលុយ។\n"
        "2️⃣ ជាជម្រើស: ចូលទៅបូតហិរញ្ញវត្ថុដើមសម្រាប់ឧបករណ៍បន្ថែម។\n\n"
        "ចុចប៊ូតុងខាងក្រោមដើម្បីបន្ត។",
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ដោះសោប៊ូតុង"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == 'tips':
        # First-time user welcome
        if user_id not in first_time_users:
            await query.message.reply_text("💡 សូមស្វាគមន៍! នេះជាគន្លឹះហិរញ្ញវត្ថុថ្មីៗរបស់អ្នក។")
            first_time_users.add(user_id)

        # Send all tips
        for tip in FINANCE_TIPS:
            await query.message.reply_text(tip)
    else:
        await query.message.reply_text("ជម្រើសមិនស្គាល់។")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ប្រើ /start ដើម្បីមើលជម្រើស។\n"
        "💡 យល់ដឹងអំពីហិរញ្ញវត្ថុ - ទទួលបានគន្លឹះប្រចាំថ្ងៃ\n"
        "🔗 ចូលទៅបូតដើម - ទៅកាន់បូតដើមរបស់យើង"
    )

# ===== DAILY TIPS JOB =====
async def daily_tips(context: ContextTypes.DEFAULT_TYPE):
    for user_id in first_time_users:
        for tip in FINANCE_TIPS:
            await context.bot.send_message(chat_id=user_id, text=f"💡 ថ្ងៃនេះគន្លឹះហិរញ្ញវត្ថុ:\n{tip}")

# ===== MAIN FUNCTION =====
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button))

    # Schedule daily tips at 9 AM
    job_queue: JobQueue = app.job_queue
    job_queue.run_daily(daily_tips, time=datetime.time(hour=9, minute=0, second=0))

    print("Bridge bot កំពុងដំណើរការ...")
    app.run_polling()

if __name__ == '__main__':
    main()
