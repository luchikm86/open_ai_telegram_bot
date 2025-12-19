import os
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from telegram import (Update, BotCommand, BotCommandScopeChat, MenuButtonCommands, InlineKeyboardButton,
                      InlineKeyboardMarkup)


# Load message from file
def load_message(name: str) -> str:
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Get message path: resources/messages/{name}.txt
    message_path = os.path.join(current_dir, 'resources', 'messages', f'{name}.txt')
    # Open message in read mode
    with open(message_path, 'r', encoding='utf-8') as file:
        return file.read()


# Send text to user
async def send_text(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    text = text.encode('utf8').decode('utf8')
    # Send message to user
    return await context.bot.send_message(
        # Id chat where send message
        chat_id=update.effective_chat.id,
        # Text message
        text=text,
        # Parse mode
        parse_mode=ParseMode.MARKDOWN
    )


# Send image to user
async def send_image(update: Update, context: ContextTypes.DEFAULT_TYPE, name: str):
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Get image path: resources/images/{name}.jpg
    image_path = os.path.join(current_dir, 'resources', 'images', f'{name}.jpg')
    # Open image in binary mode
    with open(image_path, 'rb') as image:
        return await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=image
        )


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, commands: dict):
    # Create list commands
    command_list = [
        BotCommand(command=key, description=value)
        for key, value in commands.items()
    ]
    # Set bot commands for chat
    await context.bot.set_my_commands(
        command_list,
        scope=BotCommandScopeChat(chat_id=update.effective_chat.id)
    )
    # Set menu button commands
    await context.bot.set_chat_menu_button(
        menu_button=MenuButtonCommands(),
        chat_id=update.effective_chat.id
    )


    async def load_prompt(name: str):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(current_dir, 'resources', 'prompts', f'{name}.txt')
        with open(prompt_path, 'r', encoding='utf-8') as file:
            return file.read()


    async def send_text_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, buttons: dict):
        text = text.encode('utf8', errors="surrogatepass").decode('utf8')
        keyboard = []
        for key, value in buttons.items():
            button = InlineKeyboardButton(str(value), callback_data=str(key))
            keyboard.append([button])
        reply_markup = InlineKeyboardMarkup(keyboard)
        return await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=reply_markup,
            message_thread_id=update.effective_message.message_thread_id
        )