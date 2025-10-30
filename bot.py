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
    {"question": "What is the capital of France?", "options": ["London", "Berlin", "Paris", "Madrid"], "answer": 2},
    {"question": "Which planet is known as the Red Planet?", "options": ["Venus", "Mars", "Jupiter", "Saturn"], "answer": 1},
    {"question": "What is 5 + 7?", "options": ["10", "12", "13", "11"], "answer": 1},
]

# --- START COMMAND ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_scores[user_id] = user_scores.get(user_id, 0)
    
    text = (
        "👋 Welcome to **Fun Game Hub** 🎮\n\n"
        "**Available Commands:**\n"
        "🎯 /start - Show this message\n"
        "🎮 /games - List all games\n"
        "🧠 /quiz - Start trivia quiz\n"
        "🔢 /math - Math challenge\n"
        "📊 /score - Check your score\n\n"
        "👉 Or visit our main bot:"
    )

    keyboard = [[InlineKeyboardButton("👉 Visit Main Bot 🎯", url="https://t.me/faxkh888888888bot")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)

# --- GAMES LIST ---
async def games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🎮 **Available Games:**\n\n"
        "🧠 **Quiz Game** - Test your knowledge\n"
        "• Use: /quiz\n\n"
        "🔢 **Math Challenge** - Solve math problems\n" 
        "• Use: /math\n\n"
        "📊 Track your score with /score"
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
    await update.message.reply_text(f"🧠 **Quiz Game**\n\n{question_data['question']}", reply_markup=reply_markup)

# --- MATH GAME ---  
async def math_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    answer = num1 + num2
    
    context.user_data['math_answer'] = answer
    context.user_data['game'] = 'math'
    
    await update.message.reply_text(f"🔢 **Math Challenge**\n\nWhat is {num1} + {num2}?\n\nReply with your answer!")

# --- SCORE COMMAND ---
async def score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    score = user_scores.get(user_id, 0)
    
    text = f"📊 **Your Score:** {score} points\n\nKeep playing to earn more points! 🎯"
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
                await query.edit_message_text(f"✅ **Correct!** 🎉\n\nYou earned 10 points!\n\nYour score: {user_scores[user_id]}\n\nPlay again with /quiz")
            else:
                correct_answer = question_data["options"][question_data["answer"]]
                await query.edit_message_text(f"❌ **Wrong!**\n\nThe correct answer was: {correct_answer}\n\nTry again with /quiz")

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
                await update.message.reply_text(f"✅ **Correct!** 🎉\n\nYou earned 10 points!\n\nYour score: {user_scores[user_id]}\n\nPlay again with /math")
            else:
                await update.message.reply_text(f"❌ **Wrong!**\n\nThe correct answer was: {correct_answer}\n\nTry again with /math")
        except:
            await update.message.reply_text("Please enter a valid number!")
        
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
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🎮 Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()
