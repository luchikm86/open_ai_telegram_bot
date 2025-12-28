from openai import OpenAI
import httpx

class ChatGPTService:
    client: OpenAI = None
    messages_list: list = None
    def __init__(self, token):
        self.client = OpenAI(
            http_client=httpx.Client(proxy="http://18.199.183.77:49232"),
            api_key=token
        )
        self.messages_list = []
    async def send_message_list(self) -> str:
        completion = self.client.chat.completions.create(
            # model="gpt-4o-mini",
            model="gpt-3.5-turbo",
            messages=self.messages_list,
            max_tokens=3000,
            temperature=0.9
        )
        message = completion.choices[0].message
        self.messages_list.append(message)
        return message.content

    def set_prompt(self, prompt_text: str) -> str:
        self.messages_list.clear()
        self.messages_list.append({"role": "system", "content": prompt_text})

    async def add_message(self, message_text: str) -> str:
        self.messages_list.append({"role": "user", "content": message_text})
        return await self.send_message_list()

    async def send_question(self, prompt_text: str, message_text: str) -> str:
        self.messages_list.clear()
        self.messages_list.append({"role": "system", "content": prompt_text})
        self.messages_list.append({"role": "user", "content": message_text})
        return await self.send_message_list()

    async def speech_to_text(self, audio_buffer) -> str:
        audio_buffer.name = "voice.ogg"
        transcript = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_buffer
        )
        return transcript.text

    async def text_to_speech(self, text: str) -> bytes:
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        return response.content