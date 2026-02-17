import io
import logging
from random import choice

from telegram import Update
from telegram.ext import ContextTypes

from config import CHATGPT_TOKEN
from gpt import ChatGPTService
from utils import (send_image, send_text, load_message, show_main_menu, load_prompt, send_text_buttons)

chatgpt_service = ChatGPTService(CHATGPT_TOKEN)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_image(update, context, "start")
    await send_text(update, context, load_message("start"))
    await show_main_menu(
        update,
        context,
        {
            'start': 'Головне меню',
            'random': 'Дізнатися випадковий факт',
            'gpt': 'Запитати ChatGPT',
            'talk': 'Діалог з відомою особистістю',
            'training': 'Словниковий тренажер',
        }
    )


async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_image(update, context, "random")
    message_to_delete = await send_text(update, context, "Шукаю випадковий факт ...")
    try:
        prompt = load_prompt("random")
        fact = await chatgpt_service.send_question(
            prompt_text=prompt,
            message_text="Розкажи про випадковий факт"
        )
        buttons = {
            'random': 'Хочу ще один факт',
            'start': 'Закінчити'
        }
        await send_text_buttons(update, context, fact, buttons)
    except Exception as e:
        logger.error(f"Помилка в обробнику /random: {e}")
        await send_text(update, context, "Помилка при отриманні випадкового факту.")
    finally:
        await context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=message_to_delete.message_id
        )


async def random_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == 'random':
        await random(update, context)
    elif data == 'start':
        await start(update, context)


async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await send_image(update, context, "gpt")
    chatgpt_service.set_prompt(load_prompt("gpt"))
    await send_text(update, context, "Задайте питання ...")
    context.user_data["conversation_state"] = "gpt"


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    conversation_state = context.user_data.get("conversation_state")
    if conversation_state == "gpt":
        waiting_message = await send_text(update, context, "...")
        try:
            response = await chatgpt_service.add_message(message_text)
            await send_text(update, context, response)
        except Exception as e:
            logger.error(f"Помилка при отриманні відповіді від ChatGPT: {e}")
            await send_text(update, context, "Виникла помилка при обробці вашого повідомлення.")
        finally:
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=waiting_message.message_id
            )
    if conversation_state == "talk":
        personality = context.user_data.get("selected_personality")
        if personality:
            prompt = load_prompt(personality)
            chatgpt_service.set_prompt(prompt)
        else:
            await send_text(update, context, "Спочатку оберіть особистість для розмови!")
            return
        waiting_message = await send_text(update, context, "...")
        try:
            response = await chatgpt_service.add_message(message_text)
            buttons = {"start": "Закінчити"}
            personality_name = personality.replace("talk_", "").replace("_", " ").title()
            await send_text_buttons(update, context, f"{personality_name}: {response}", buttons)
        except Exception as e:
            logger.error(f"Помилка при отриманні відповіді від ChatGPT: {e}")
            await send_text(update, context, "Виникла помилка при отриманні відповіді!")
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=waiting_message.message_id)
        finally:
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=waiting_message.message_id
            )
    if conversation_state == "training_test":
        index = context.user_data.get("current_word_index", 0)
        words = context.user_data.get("words_list", [])
        correct_info = words[index]

        prompt = load_prompt("training_test")

        check_result = await chatgpt_service.send_question(
            prompt_text=prompt,
            message_text=f"Картка: {correct_info}. Відповідь користувача: {message_text}"
        )
        if "ТАК" in check_result.upper():
            context.user_data["test_score"] += 1
            await send_text(update, context, "✅ Правильно!")
        else:
            await send_text(update, context, f"❌ Не зовсім. \nОригінал: {correct_info}")

        context.user_data["current_word_index"] += 1
        await run_test_step(update, context)
        return
    if not conversation_state:
        intent_recognized = await inter_random_input(update, context, message_text)
        if not intent_recognized:
            await show_funny_response(update, context)
        return


async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await send_image(update, context, "talk")
    personalities = {
        'talk_linus_torvalds': "Linus Torvalds (Linux, Git)",
        'talk_guido_van_rossum': "Guido van Rossum (Python)",
        'talk_mark_zuckerberg': "Mark Zuckerberg (Meta, Facebook)",
        'start': "Закінчити",
    }
    await send_text_buttons(update, context, "Оберіть особистість для спілкування ...", personalities)


async def talk_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "start":
        context.user_data.pop("conversation_state", None)
        context.user_data.pop("selected_personality", None)
        await start(update, context)
        return
    if data.startswith("talk_"):
        context.user_data.clear()
        context.user_data["selected_personality"] = data
        context.user_data["conversation_state"] = "talk"
        prompt = load_prompt(data)
        chatgpt_service.set_prompt(prompt)
        personality_name = data.replace("talk_", "").replace("_", " ").title()
        await send_image(update, context, data)
        buttons = {'start': "Закінчити"}
        await send_text_buttons(
            update,
            context,
            f"Hello, I`m {personality_name}."
            f"\nI heard you wanted to ask me something. "
            f"\nYou can ask questions in your native language.",
            buttons
        )


async def inter_random_input(update: Update, context: ContextTypes.DEFAULT_TYPE, message_text):
    message_text_lower = message_text.lower()
    if any(keyword in message_text_lower for keyword in ['факт', 'цікав', 'random', 'випадков']):
        await send_text(
            update,
            context,
            text="Схоже, ви цікавитесь випадковими фактами! Зараз покажу вам один..."
        )
        await random(update, context)
        return True

    elif any(keyword in message_text_lower for keyword in ['gpt', 'чат', 'питання', 'запита', 'дізнатися']):
        await send_text(
            update,
            context,
            text="Схоже, у вас є питання! Переходимо до режиму спілкування з ChatGPT..."
        )
        await gpt(update, context)
        return True

    elif any(keyword in message_text_lower for keyword in ['розмов', 'говори', 'спілкува', 'особист', 'talk']):
        await send_text(
            update,
            context,
            text="Схоже, ви хочете поговорити з відомою особистістю! Зараз покажу вам доступні варіанти..."
        )
        await talk(update, context)
        return True
    return False


async def show_funny_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    funny_responses = [
        "Хмм... Цікаво, але я не зрозумів, що саме ви хочете. Може спробуєте одну з команд з меню?",
        "Дуже цікаве повідомлення! Але мені потрібні чіткіші інструкції. Ось доступні команди:",
        "Ой, здається, ви мене застали зненацька! Я вмію багато чого, але мені потрібна конкретна команда:",
        "Вибачте, мої алгоритми не розпізнали це як команду. Ось що я точно вмію:",
        "Це повідомлення таке ж загадкове, як єдиноріг у дикій природі! Спробуйте одну з цих команд:",
        "Я намагаюся зрозуміти ваше повідомлення... Але краще скористайтесь однією з команд:",
        "О! Випадкове повідомлення! Я теж вмію бути випадковим, але краще використовуйте команди:",
        "Гм, не спрацювало. Може спробуємо ці команди?",
        "Це повідомлення прекрасне, як веселка! Але для повноцінного спілкування спробуйте:",
        "Згідно з моїми розрахунками, це повідомлення не відповідає жодній з моїх команд. Ось вони:",
    ]
    random_response = choice(funny_responses)
    available_commands = """
    - Не знаєте, що обрати? Почніть з /start,
    - Спробуйте команду /gpt, щоб задати питання,
    """
    full_message = f"{random_response}\n{available_commands}"
    await update.message.reply_text(full_message)


async def handle_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not  update.message.voice:
        return

    await context.bot.send_chat_action(
        chat_id=update.message.chat_id,
        action='record_voice'
    )

    try:
        voice_file = await update.message.voice.get_file()
        voice_bytearray = await voice_file.download_as_bytearray()
        audio_buffer = io.BytesIO(voice_bytearray)

        user_text = await chatgpt_service.speech_to_text(audio_buffer)

        state = context.user_data.get("conversation_state")

        if state == "talk":
            personality = context.user_data.get("selected_personality")
            chatgpt_service.set_prompt(load_prompt(personality))
        else:
            chatgpt_service.set_prompt(load_prompt("gpt"))
            context.user_data["conversation_state"] = "gpt"
        gpt_response_text = await chatgpt_service.add_message(user_text)

        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action='record_voice'
        )
        audio_answer = await chatgpt_service.text_to_speech(gpt_response_text)

        await update.message.reply_voice(
            voice=io.BytesIO(audio_answer),
        )

    except Exception as e:
        logger.error(f"Помилка обробки голосового повідомлення: {e}")
        await  update.message.reply_text("Вибачте, сталася помилка при обробці голосового повідомлення.")


async def training(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["conversation_state"] = "training"
    if "words_list" not in context.user_data:
        context.user_data['words_list'] = []

    await send_image(update, context, "training")
    await training_next_word(update, context)


async def training_next_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    words = context.user_data.get("words_list", [])

    if len(words) >= 10:
        await send_text(update, context, "💪 Ти вже назбирав **10 слів**! Це ідеальна порція для тренування. "
                                         "Давай перевіримо твої знання?")
        buttons = {
            'training_test': '🚀 Почати тест',
            'start': 'Закінчити'
        }
        await send_text_buttons(update, context, "Натисни кнопку нижче, щоб розпочати тест:", buttons)
        return

    waiting_message = await send_text(update, context, "Генерую нове слово... 🧠")
    try:
        prompt = load_prompt("training")
        word = await chatgpt_service.send_question(
            prompt_text=prompt,
            message_text="Дай мені нове слово для вивчення."
        )
        context.user_data["words_list"].append(word)
        current_word = len(context.user_data["words_list"])

        buttons = {
            'training_more': f'Ще слово ({current_word}/10)',
            'training_test': 'Тренуватися (Тест)',
            'start': 'Закінчити'
        }

        await send_text_buttons(update, context, word, buttons)
    finally:
        await context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=waiting_message.message_id
        )


async def training_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == 'training_more':
        await training_next_word(update, context)
    elif data == 'training_test':
        await start_test(update, context)


async def start_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    words = context.user_data.get("words_list", [])
    if not words:
        await send_text(update, context, "❌ Твій словник порожній. Спочатку вивчи кілька слів!")
        return
    context.user_data["test_score"] = 0
    context.user_data["current_word_index"] = 0
    context.user_data["conversation_state"] = "training_test"

    await send_text(update, context, f"🚀 Починаємо тест! У тебе {len(words)} слів. Успіхів!")
    await run_test_step(update, context)


async def run_test_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    index = context.user_data.get("current_word_index")
    words = context.user_data.get("words_list")
    if index < len(words):
        full_info = words[index]
        word_to_test = full_info.split('-')[0].strip()
        await send_text(update, context, f"Слово №{index + 1}: **{word_to_test}**\n\nНапиши переклад:")
    else:
        score = context.user_data.get("test_score")
        total = len(words)
        await send_text(update, context, f"🏁 Тест завершено!\nТвій результат: {score} з {total} ✅")
        context.user_data["conversation_state"] = "training"

        buttons = {
            'training_more': 'Вчити ще слова',
            'start': 'В головне меню'
        }
        await send_text_buttons(update, context, "Бажаєш продовжити?", buttons)