from typing import List
from modules.llm.llm_client import LLMClient
from modules.llm.types import Chat, Pal


class PrototypeLLMClient(LLMClient):
    def __init__(self):
        super().__init__()

    def get_chat_response(self, chats: List[Chat], bot_name: str, bot_bg: str, writing_prompt: str) -> str:
        return "This is a hardcoded chat response."

    def summarize_chat(self, chats: List[Chat], bot_name: str) -> str:
        return "This is a summary of the chat."

    def generate_pals(self, prompt: str) -> Pal:
        return Pal(name="John Doe", occupation="Writer", description="This is a hard coded PAL.")

    def get_language_suggestion(self, writing: str) -> str:
        return "The language is very very good, this is hard coded"

    def get_content_suggestion(self, writing: str) -> str:
        return "The content is very very good, this is hard coded"

    def get_organization_suggestion(self, writing: str) -> str:
        return "The organization is very very good, this is hard coded"