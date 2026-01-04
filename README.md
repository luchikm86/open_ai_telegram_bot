# Telegram ChatGPT Bot

A versatile Telegram bot that integrates with OpenAI's ChatGPT to provide various interactive features.

![start.jpg](src/resources/images/start.jpg)

---

### ✔ Core Features:

### ✔ Core Features:

-   **Voice-to-Voice Chat** - Full audio interaction using OpenAI Whisper (STT) and OpenAI TTS
-   **Random Fact Generator** - Get interesting facts with AI-generated content
-   **ChatGPT Interface** - Direct chat with OpenAI's ChatGPT (now using gpt-4o-mini)
-   **Celebrity Chat** - Chat with AI personalities (Linus Torvalds, Guido van Rossum, Mark Zuckerberg)


### ✔ Voice Processing Workflow
The bot implements a sophisticated audio processing pipeline:
1. **Speech-to-Text**: Converts incoming `.ogg` voice messages to text using `whisper-1`.
2. **AI Generation**: Processes the request using `gpt-4o-mini` with context awareness.
3. **Text-to-Speech**: Converts the response back to audio via `tts-1` using the `alloy` voice.
4. **Memory Efficient**: All audio is processed in-memory using `io.BytesIO` buffers.


### ✔ Optional Features (Choose 2+)

-   Language Translator
-   Voice ChatGPT
-   Movie/Book Recommendations
-   Vocabulary Trainer
-   Image Recognition
-   Resume Assistant

---

![random.jpg](src/resources/images/random.jpg)

### ✔ Prerequisites

-   Python 3.8+
-   Telegram Bot Token
-   OpenAI API Key
-   Required Python packages (see `requirements.txt`)

---

### ✔ Installation

Clone the repository:

```
git clone <repository-url>
cd open_ai_telegram_bot_group_6
```

Create and activate a virtual environment:

```
python -m venv venv
source venv/bin/activate  # On Windows: venvScriptsactivate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root and add your tokens:

```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
```

---

### ✔ Usage

Start the bot:

```bash
python src/bot.py
```

In Telegram, find your bot using the username you set up and start a chat.

Available commands:

-   `/start` - Start the bot
-   `/random` - Get a random fact
-   `/gpt` - Chat with ChatGPT
-   `/talk` - Chat with a celebrity personality
-   **Voice Messages** - Send a voice message to get an audio response from the AI

![gpt.jpg](src/resources/images/gpt.jpg)

---

### ✔ Project Structure

```
open_ai_telegram_bot
├── .env.example         # Example environment variables
├── .gitignore           # Git ignore file
├── README.md            # This file
├── requirements.txt     # Project dependencies
└── src/
    ├── bot.py           # Main bot application
    ├── config.py        # Configuration settings
    ├── gpt.py           # GPT integration module
    ├── handlers.py      # Bot command handlers
    ├── utils.py         # Utility functions
    └── resources/       # Resource files
        ├── images/      # Image assets for the bot
        ├── messages/    # Message templates
        │   └── start.txt
        └── prompts/     # AI prompt templates
            ├── gpt.txt
            ├── random.txt
            ├── talk_guido_van_rossum.txt
            ├── talk_linus_torvalds.txt
            └── talk_mark_zuckerberg.txt
```

---

### ✔ Environment Variables

The following environment variables need to be set:

-   `TELEGRAM_BOT_TOKEN`: Your Telegram Bot Token from @BotFather
-   `OPENAI_API_KEY`: Your OpenAI API key

---

### ✔ Contributing

-   Fork the repository
-   Create a new branch for your feature
-   Commit your changes
-   Push to the branch
-   Create a new Pull Request

---

### ✔ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---