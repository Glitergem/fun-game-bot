import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
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
    {"question": "Which animal is known as the King of Jungle?", "options": ["Elephant", "Lion", "Tiger", "Giraffe"], "answer": 1},
    {"question": "How many continents are there?", "options": ["5", "6", "7", "8"], "answer": 2}
]

math_questions = [
    {"question": "8 × 7 = ?", "answer": "56"},
    {"question": "15 + 23 = ?", "answer": "38"},
    {"question": "64 ÷ 8 = ?", "answer": "8"},
    {"question": "12 × 4 = ?", "answer": "48"},
    {"question": "45 - 18 = ?", "answer": "27"}
]

word_list = ["python", "telegram", "keyboard", "gaming", "bot", "code", "render", "github"]

# --- START COMMAND ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_scores[user_id] = user_scores.get(user_id, 0)
    
    text = (
        "👋 សួស្តី! ស្វាគមន៍មកកាន់ **Fun Game Hub** 🎮\n"
        "នៅទីនេះអ្នកអាចសាកល្បងហ្គេមសប្បាយៗ និងស្វែងយល់អំពីបូតថ្មីៗ។\n\n"
        "👋 Welcome to **Fun Game Hub!** 🎮\n"
        "Discover fun mini-games and explore new Telegram bots every day!\n\n"
        "**Available Commands:**\n"
        "🎯 /start - Show this welcome message\n"
        "🎮 /games - List all available games\n"
        "🧠 /quiz - Start a trivia quiz\n"
        "🔢 /math - Math challenge game\n"
        "🔠 /word - Word guessing game\n"
        "📊 /score - Check your score\n"
        "ℹ️ /help - How to play\n\n"
        "👉 Or visit our main bot:"
    )

    keyboard = [[InlineKeyboardButton("👉 Visit Main Bot 🎯", url="https://t.me/faxkh888888888bot")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)

# --- GAMES LIST ---
async def games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🎮 **Available Games:**\n\n"
        "🧠 **Quiz Game** - Test your knowledge with fun trivia questions\n"
        "• Use: /quiz\n\n"
        "🔢 **Math Challenge** - Solve quick math problems\n" 
        "• Use: /math\n\n"
        "🔠 **Word Guesser** - Guess the hidden word\n"
        "• Use: /word\n\n"
        "📊 **Track your progress** with /score"
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
    question_data = random.choice(math_questions)
    context.user_data['current_question'] = question_data
    context.user_data['game'] = 'math'
    
    await update.message.reply_text(f"🔢 **Math Challenge**\n\n{question_data['question']}\n\nReply with your answer!")

# --- WORD GAME ---
async def word_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    word = random.choice(word_list)
    hidden_word = "🔴" * len(word)
    context.user_data['current_word'] = word
    context.user_data['hidden_word'] = hidden_word
    context.user_data['attempts'] = 5
    context.user_data['game'] = 'word'
    
    text = (
        f"🔠 **Word Guesser**\n\n"
        f"Word: {hidden_word}\n"
        f"Length: {len(word)} letters\n"
        f"Attempts left: 5\n\n"
        f"Guess a letter or the whole word!"
    )
    await update.message.reply_text(text)

# --- SCORE COMMAND ---
async def score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    score = user_scores.get(user_id, 0)
    
    text = f"📊 **Your Score:** {score} points\n\nKeep playing to earn more points! 🎯"
    await update.message.reply_text(text, parse_mode="Markdown")

# --- HELP COMMAND ---
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "ℹ️ **How to Play:**\n\n"
        "🎮 Use /games to see all available games\n"
        "🧠 /quiz - Multiple choice trivia\n" 
        "🔢 /math - Solve math problems\n"
        "🔠 /word - Guess hidden words\n"
        "📊 /score - Check your progress\n\n"
        "**Earn points** for correct answers and compete with friends!"
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
                await query.edit_message_text(f"✅ **Correct!** 🎉\n\nYou earned 10 points!\n\nYour score: {user_scores[user_id]}\n\nPlay again with /quiz")
            else:
                correct_answer = question_data["options"][question_data["answer"]]
                await query.edit_message_text(f"❌ **Wrong!**\n\nThe correct answer was: {correct_answer}\n\nTry again with /quiz")

# --- HANDLE TEXT MESSAGES (for math and word games) ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text.strip().lower()
    game_type = context.user_data.get('game')
    
    if game_type == 'math':
        question_data = context.user_data.get('current_question')
        if question_data and user_text == question_data['answer'].lower():
            user_scores[user_id] = user_scores.get(user_id, 0) + 10
            await update.message.reply_text(f"✅ **Correct!** 🎉\n\nYou earned 10 points!\n\nYour score: {user_scores[user_id]}\n\nPlay again with /math")
            context.user_data['game'] = None
        elif question_data:
            await update.message.reply_text(f"❌ **Wrong!**\n\nThe correct answer was: {question_data['answer']}\n\nTry again with /math")
            context.user_data['game'] = None
    
    elif game_type == 'word':
        word = context.user_data.get('current_word', '')
        hidden_word = context.user_data.get('hidden_word', '')
        attempts = context.user_data.get('attempts', 5)
        
        if user_text == word.lower():
            user_scores[user_id] = user_scores.get(user_id, 0) + 20
            await update.message.reply_text(f"🎉 **Congratulations!** 🎉\n\nYou guessed the word: **{word}**\n\nYou earned 20 points!\n\nYour score: {user_scores[user_id]}\n\nPlay again with /word")
            context.user_data['game'] = None
        elif len(user_text) == 1 and user_text.isalpha():
            # Single letter guess
            if user_text in word.lower():
                # Reveal the letter
                new_hidden = ""
                for i, char in enumerate(word.lower()):
                    if char == user_text or hidden_word[i] != '🔴':
                        new_hidden += word[i]
                    else:
                        new_hidden += '🔴'
                
                context.user_data['hidden_word'] = new_hidden
                
                if new_hidden == word:
                    user_scores[user_id] = user_scores.get(user_id, 0) + 20
                    await update.message.reply_text(f"🎉 **Congratulations!** 🎉\n\nYou guessed the word: **{word}**\n\nYou earned 20 points!\n\nYour score: {user_scores[user_id]}\n\nPlay again with /word")
                    context.user_data['game'] = None
                else:
                    await update.message.reply_text(f"✅ **Good guess!**\n\nWord: {new_hidden}\n\nAttempts left: {attempts}\n\nKeep guessing!")
            else:
                attempts -= 1
                context.user_data['attempts'] = attempts
                if attempts > 0:
                    await update.message.reply_text(f"❌ **Letter not found**\n\nWord: {hidden_word}\n\nAttempts left: {attempts}\n\nTry another letter!")
                else:
                    await update.message.reply_text(f"💀 **Game Over!**\n\nThe word was: **{word}**\n\nTry again with /word")
                    context.user_data['game'] = None
        else:
            await update.message.reply_text("Please guess a single letter or the whole word!")

# --- RUN BOT ---
def main():
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("games", games))
    application.add_handler(CommandHandler("quiz", quiz))
    application.add_handler(CommandHandler("math", math_game))
    application.add_handler(CommandHandler("word", word_game))
    application.add_handler(CommandHandler("score", score))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(telegram.ext.MessageHandler(telegram.ext.filters.TEXT & ~telegram.ext.filters.COMMAND, handle_message))
    
    print("🎮 Fun Game Hub Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()
