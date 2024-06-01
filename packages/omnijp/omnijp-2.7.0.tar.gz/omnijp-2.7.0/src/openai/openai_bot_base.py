from abc import abstractmethod

import openai


class OpenAIBotBase:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = None

    def get_response(self, response):
        return response.choices[0].message.content.strip()

    @staticmethod
    def create_message(prompt):
        return [{"role": "user", "content": prompt},
                {"role": "system",
                 "content": "You are a helpful assistant that provides concise and accurate information."}]

    @staticmethod
    def handle_error(self, error):
        error_messages = {
            openai.RateLimitError: "Rate limit exceeded. Please try again later.",
            openai.AuthenticationError: "Authentication failed. Please check your API key.",
            openai.OpenAIError: "An error occurred."
        }

        error_type = type(error)
        message = error_messages.get(error_type, "An unknown error occurred.")
        raise Exception(message, error)
