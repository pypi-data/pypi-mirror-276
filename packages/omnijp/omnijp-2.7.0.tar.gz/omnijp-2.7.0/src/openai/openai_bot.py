from openai import OpenAI
from src.openai.openai_bot_base import OpenAIBotBase


class OpenAIBot(OpenAIBotBase):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.client = OpenAI(api_key=api_key)

    def get_response(self, prompt: str, model: str = "gpt-3.5-turbo"):
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=self.create_message(prompt))
            return super().get_response(response)
        except Exception as e:
            self.handle_error(e)
            return None


