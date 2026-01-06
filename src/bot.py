from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters

from config import BOT_TOKEN
from handlers import (start, random, random_button, gpt, message_handler, talk, talk_button, handle_voice_message,
                      training, training_button)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("random", random))
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(CommandHandler("talk", talk))
app.add_handler(CommandHandler("training", training))
app.add_handler(CallbackQueryHandler(random_button, pattern='^(random|start)$'))
app.add_handler(
    CallbackQueryHandler(talk_button, pattern='^(talk_linus_torvalds|talk_guido_van_rossum|talk_mark_zuckerberg)$'))
app.add_handler(CallbackQueryHandler(training_button, pattern='^(training_more|training_test)$'))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
app.add_handler(MessageHandler(filters.VOICE, handle_voice_message))

app.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)