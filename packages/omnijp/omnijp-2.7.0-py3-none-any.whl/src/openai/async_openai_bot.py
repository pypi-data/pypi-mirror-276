from openai import AsyncOpenAI
from typing import Callable, Any
from src.openai.openai_bot_base import OpenAIBotBase


class AsyncOpenAIBot(OpenAIBotBase):

    def __init__(self, api_key):
        super().__init__(api_key)
        self.client = AsyncOpenAI(api_key=api_key)

    async def get_response_async(self, prompt: str, callback: Callable[[Any], None], model: str = "gpt-3.5-turbo"):
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=self.create_message(prompt))
            callback(super().get_response(response))
        except Exception as e:
            self.handle_error(e)

