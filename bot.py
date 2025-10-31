from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ===== CONFIG =====
TOKEN = "8122545395:AAEPRCfDKZquAlgXMcuzLyF78MB9_vU-FJw"
MAIN_BOT_LINK = "https://t.me/faxkh888888888bot"

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

    if query.data == 'tips':
        tips = [
            "💰 គន្លឹះ ១: តែងតែសន្សំពេលអតិថិជន ១០% នៃចំណូលរបស់អ្នក។",
            "📊 គន្លឹះ ២: តាមដានចំណាយប្រចាំសប្តាហ៍ដើម្បីរកកន្លែងចំណាយចេញមិនចាំបាច់។",
            "🏦 គន្លឹះ ៣: ចែកចាយការសន្សំរបស់អ្នករវាងគោលបំណងខ្លី និងវែង។",
            "📈 គន្លឹះ ៤: គួរជៀសវាងបំណុលដែលមានការប្រាក់ខ្ពស់។"
        ]
        for tip in tips:
            await query.message.reply_text(tip)
    else:
        await query.message.reply_text("ជម្រើសមិនស្គាល់។")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ប្រើ /start ដើម្បីមើលជម្រើស។")

# ===== MAIN FUNCTION =====
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button))

    print("Bridge bot កំពុងដំណើរការ...")
    app.run_polling()

if __name__ == '__main__':
    main()
