from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

from config import BOT_TOKEN
from handlers import start

# Create object Telegram-bot
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Add handler command start
app.add_handler(CommandHandler("start", start))

# Run bot
app.run_polling(
    drop_pending_updates=True,
    allowed_updates=Update.ALL_TYPES,
)