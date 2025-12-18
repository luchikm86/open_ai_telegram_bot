from openai import OpenAI
import httpx

class ChatGPTService:

    # Client OpenAI
    client: OpenAI = None

    # List messages
    messages_list: list = None

    # Constructor
    def __init__(self, token):

        # Create client OpenAI
        self.client = OpenAI(
            http_client=httpx.Client(proxy="http://18.199.183.77:49232"),
            api_key=token
        )

        # Create list messages
        self.messages_list = []

    # Send message list in ChatGPT
    async def send_message_list(self) -> str:
        completion = await self.client.chat.completions.create(
            # Model ChatGPT
            model="gpt-3.5-turbo",
            # Messages list(history chat)
            messages=self.messages_list,
            # Max length answer in tokens
            max_tokens=3000,
            # Degree of creativity of the answer
            # 0.9 - answers will be diverse and creative
            temperature=0.9
        )
        # Add the received message to the chat history
        message = completion.choices[0].message

        # Add message to list messages
        self.messages_list.append(message)

        # Return message from ChatGPT
        return message.content

    def set_prompt(self, prompt_text: str) -> str:
        # Clear list messages
        self.messages_list.clear()
        # Add message to list messages
        self.messages_list.append({"role": "system", "content": prompt_text})

    async def add_message(self, message_text: str) -> str:
        # Add message to list messages
        self.messages_list.append({"role": "user", "content": message_text})
        # Send message list in ChatGPT
        return await self.send_message_list()

    async def send_question(self, prompt_text: str, message_text: str) -> str:
        # Clear history messages
        self.messages_list.clear()
        # Add system message
        self.messages_list.append({"role": "system", "content": prompt_text})
        # Add user message
        self.messages_list.append({"role": "user", "content": message_text})
        return await self.send_message_list()