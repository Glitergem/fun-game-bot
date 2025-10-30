import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters
import os

# --- CONFIGURATION ---
TOKEN = "8122545395:AAEPRCfDKZquAlgXMcuzLyF78MB9_vU-FJw"

# --- SETUP ---
logging.basicConfig(level=logging.INFO)

# Game data
user_scores = {}

quiz_questions = [
    {"question": "តើរដ្ឋធានីរបស់បារាំងគឺជាអ្វី?", "options": ["ឡុងដ៍", "ប៊ែរឡីន", "ប៉ារីស", "ម៉ាឌ្រីដ"], "answer": 2},
    {"question": "តើភពណាដែលត្រូវបានគេស្គាល់ថាជាភពក្រហម?", "options": ["ភពសុក្រ", "ភពអង្គារ", "ភពព្រហស្បតិ៍", "ភពសៅរ៍"], "answer": 1},
    {"question": "តើ ៥ + ៧ ស្មើប៉ុន្មាន?", "options": ["១០", "១២", "១៣", "១១"], "answer": 1},
    {"question": "តើសត្វអ្វីដែលត្រូវបានគេស្គាល់ថាជាស្តេចព្រៃ?", "options": ["ដំរី", "សិង្ហ", "ខ្លាធំ", "រមាំង"], "answer": 1},
    {"question": "តើមានទ្វីបប៉ុន្មាន?", "options": ["៥", "៦", "៧", "៨"], "answer": 2}
]

# --- START COMMAND ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_scores[user_id] = user_scores.get(user_id, 0)
    
    text = (
        "👋 សួស្តី! ស្វាគមន៍មកកាន់ **Fun Game Hub** 🎮\n\n"
        "**ពាក្យបញ្ជា:**\n"
        "🎯 /start - បង្ហាញសារស្វាគមន៍\n"
        "🎮 /games - បង្ហាញហ្គេមទាំងអស់\n"
        "🧠 /quiz - ចាប់ផ្តើមល្បែងចម្លើយ\n"
        "🔢 /math - ប្រកួតគណិតវិទ្យា\n"
        "📊 /score - ពិនិត្យពិន្ទុរបស់អ្នក\n\n"
        "👉 ឬទស្សនាបូតចម្បងរបស់យើង៖"
    )

    keyboard = [[InlineKeyboardButton("👉 ទស្សនាបូតចម្បង 🎯", url="https://t.me/faxkh888888888bot")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)

# --- GAMES LIST ---
async def games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🎮 **ហ្គេមដែលមាន៖**\n\n"
        "🧠 **ល្បែងចម្លើយ** - សាកល្បងចំណេះដឹងរបស់អ្នក\n"
        "• ប្រើ: /quiz\n\n"
        "🔢 **ប្រកួតគណិតវិទ្យា** - ដោះស្រាយបញ្ហាគណិតវិទ្យា\n" 
        "• ប្រើ: /math\n\n"
        "📊 តាមដានពិន្ទុរបស់អ្នកជាមួយ /score"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

# --- QUIZ GAME ---
async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question_data = random.choice(quiz_questions)
    context.user_data['current_question'] = question_data
    context.user_data['game'] = 'quiz'
    
    keyboard = []
    for i, option in enumerate(question_data["options"]):
        keyboard.append([InlineKeyboardButton(option, callback_data=f"answer_{i}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"🧠 **ល្បែងចម្លើយ**\n\n{question_data['question']}", reply_markup=reply_markup)

# --- MATH GAME ---  
async def math_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    answer = num1 + num2
    
    context.user_data['math_answer'] = answer
    context.user_data['game'] = 'math'
    
    await update.message.reply_text(f"🔢 **ប្រកួតគណិតវិទ្យា**\n\nតើ {num1} + {num2} ស្មើប៉ុន្មាន?\n\nឆ្លើយតបជាមួយចម្លើយរបស់អ្នក!")

# --- SCORE COMMAND ---
async def score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    score = user_scores.get(user_id, 0)
    
    text = f"📊 **ពិន្ទុរបស់អ្នក:** {score} ពិន្ទុ\n\nបន្តលេងដើម្បីរកពិន្ទុបន្ថែម! 🎯"
    await update.message.reply_text(text, parse_mode="Markdown")

# --- HELP COMMAND ---
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "ℹ️ **របៀបលេង:**\n\n"
        "🎮 ប្រើ /games ដើម្បីមើលហ្គេមទាំងអស់\n"
        "🧠 /quiz - ចម្លើ�ពហុជម្រើស\n" 
        "🔢 /math - ដោះស្រាយបញ្ហាគណិតវិទ្យា\n"
        "📊 /score - ពិនិត្យការរីកលូតលាស់របស់អ្នក\n\n"
        "**រកពិន្ទុ** សម្រាប់ចម្លើយត្រឹមត្រូវ និងប្រកួតជាមួយមិត្តភក្តិ!"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

# --- HANDLE CALLBACKS ---
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data
    
    if data.startswith("answer_"):
        answer_index = int(data.split("_")[1])
        question_data = context.user_data.get('current_question')
        
        if question_data and context.user_data.get('game') == 'quiz':
            if answer_index == question_data["answer"]:
                user_scores[user_id] = user_scores.get(user_id, 0) + 10
                await query.edit_message_text(f"✅ **ត្រឹមត្រូវ!** 🎉\n\nអ្នកបានរកឃើញ ១០ ពិន្ទុ!\n\nពិន្ទុរបស់អ្នក: {user_scores[user_id]}\n\nលេងម្តងទៀតជាមួយ /quiz")
            else:
                correct_answer = question_data["options"][question_data["answer"]]
                await query.edit_message_text(f"❌ **ខុស!**\n\nចម្លើយត្រឹមត្រូវគឺ: {correct_answer}\n\nព្យាយាមម្តងទៀតជាមួយ /quiz")

# --- HANDLE TEXT MESSAGES ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Only handle if it's not a command
    if update.message.text.startswith('/'):
        return
        
    user_id = update.effective_user.id
    user_text = update.message.text.strip()
    game_type = context.user_data.get('game')
    
    if game_type == 'math':
        try:
            user_answer = int(user_text)
            correct_answer = context.user_data.get('math_answer')
            
            if user_answer == correct_answer:
                user_scores[user_id] = user_scores.get(user_id, 0) + 10
                await update.message.reply_text(f"✅ **ត្រឹមត្រូវ!** 🎉\n\nអ្នកបានរកឃើញ ១០ ពិន្ទុ!\n\nពិន្ទុរបស់អ្នក: {user_scores[user_id]}\n\nលេងម្តងទៀតជាមួយ /math")
            else:
                await update.message.reply_text(f"❌ **ខុស!**\n\nចម្លើយត្រឹមត្រូវគឺ: {correct_answer}\n\nព្យាយាមម្តងទៀតជាមួយ /math")
        except:
            await update.message.reply_text("សូមបញ្ចូលលេខត្រឹមត្រូវ!")
        
        context.user_data['game'] = None

# --- RUN BOT ---
def main():
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("games", games))
    application.add_handler(CommandHandler("quiz", quiz))
    application.add_handler(CommandHandler("math", math_game))
    application.add_handler(CommandHandler("score", score))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🎮 Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()
