import logging
import os
import random
from dotenv import load_dotenv
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ====== LOAD TOKEN ======
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN") or "8122545395:AAEPRCfDKZquAlgXMcuzLyF78MB9_vU-FJw"
MAIN_BOT_LINK = "https://t.me/faxkh888888888bot"

# ====== FINANCE TIPS ======
FINANCE_TIPS = [
    "💡 គន្លឹះទី១៖ ចាប់ផ្តើមរក្សាសន្សំ ១០% នៃប្រាក់ចំណូលរាល់ខែ។",
    "💡 គន្លឹះទី២៖ កុំខ្ចីលុយដើម្បីទិញអ្វីដែលមិនចាំបាច់។",
    "💡 គន្លឹះទី៣៖ បង្កើនចំណេះដឹងហិរញ្ញវត្ថុជារៀងរាល់ថ្ងៃ។",
    "💡 គន្លឹះទី៤៖ ចំណាយតិចជាងប្រាក់ចំណូលរបស់អ្នក។",
    "💡 គន្លឹះទី៥៖ វិនិយោគលើការអប់រំ និងជំនាញរបស់អ្នក។",
]

# Keep track of users who received the intro message
first_time_users = set()

# ====== LOGGING ======
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelna
