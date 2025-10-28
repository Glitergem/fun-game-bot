import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_USERNAME = os.getenv('BOT_USERNAME', '@fungamehubbot')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with instructions when the command /start is issued."""
    
    # Create keyboard with username button
    keyboard = [
        [InlineKeyboardButton("🎮 Click here to start the bot! 🎮", url=f"https://t.me/{BOT_USERNAME[1:]}?start=start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Welcome message with instructions
    message_text = f"""
🎮 **Welcome to FunGame Hub Bot!** 🎮

To get started with our amazing games and features, you need to click our username below:

**{BOT_USERNAME}**

Or simply click the button below to properly start the bot and unlock all the fun!

👇 **Click the button below to begin** 👇
    """
    
    await update.message.reply_text(
        text=message_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the button click."""
    query = update.callback_query
    
    # Answer the callback query
    await query.answer("Starting the bot...")
    
    # Send welcome message when button is clicked
    welcome_text = """
🎉 **Welcome to FunGame Hub Bot!** 🎉

Now that you've properly started the bot, here's what you can do:

🕹️ **Play Games** - Enjoy various fun games
🏆 **Compete** - Challenge other players  
📊 **Leaderboards** - See top scores
🎯 **Daily Challenges** - New games every day

Use /help to see all available commands!

Let the fun begin! 🎮
    """
    
    await query.edit_message_text(
        text=welcome_text,
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
🤖 **FunGame Hub Bot Commands:**

/start - Start the bot and see instructions
/help - Show this help message  
/games - Browse available games
/profile - View your gaming profile
/leaderboard - See top players

🎮 **Ready to play? Let's get gaming!**
    """
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle any message that is not a command."""
    # If someone sends a regular message, guide them to use /start
    await update.message.reply_text(
        "👋 Hello! Use /start to begin using the FunGame Hub Bot!",
        parse_mode='Markdown'
    )

def main() -> None:
    """Start the bot."""
    if not BOT_TOKEN:
        logger.error("No BOT_TOKEN found in environment variables!")
        return
    
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(CommandHandler("help", help_command))
    
    # Add handler for non-command messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the Bot
    logger.info("Bot is starting...")
    application.run_polling()
    logger.info("Bot is running!")

if __name__ == '__main__':
    main()
