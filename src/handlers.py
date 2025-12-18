import logging
from telegram import Update
from telegram.ext import ContextTypes, CallbackContext

from utils import send_image, send_text, load_message, show_main_menu
from gpt import ChatGPTService
from config import CHATGPT_TOKEN

# Create object ChatGPTService
chatgpt_service = ChatGPTService(CHATGPT_TOKEN)

# Configuring the basic logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Create object logger
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Send image user
    await send_image(update, context, "start")

    # Send text user
    await send_text(update, context, load_message("start"))

    # Show main menu
    await show_main_menu(
        update,
        context,
        {
            'start': 'Головне меню',
            'random': 'Дізнатися випадковий факт',
            'gpt': 'Запитати ChatGPT',
            'talk': 'Діалог з відомою особистістю',
            'quiz': 'Перевірити свої знання'
        }
    )