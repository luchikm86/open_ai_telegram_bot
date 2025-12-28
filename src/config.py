import os
import tempfile
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

CHATGPT_TOKEN = os.getenv("CHATGPT_TOKEN")
BOT_TOKEN = os.getenv("BOT_TOKEN")