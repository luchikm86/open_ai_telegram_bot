from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

from config import BOT_TOKEN
from handlers import start
from handlers import start, random, random_button

# Create object Telegram-bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
# Add handler command start
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("random", random))
app.add_handler(CallbackQueryHandler(random_button))

# Run bot
app.run_polling(
    drop_pending_updates=True,
    allowed_updates=Update.ALL_TYPES,
)