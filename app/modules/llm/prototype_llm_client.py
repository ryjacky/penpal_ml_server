from typing import List
from modules.llm.llm_client import LLMClient
from modules.llm.types import Chat


class PrototypeLLMClient(LLMClient):
    def __init__(self):
        pass

    def get_chat_response(self, chats: List[Chat]) -> str:
        return "This is a hardcoded chat response."

    def summarize_chat(self, chats: List[Chat]) -> str:
        return "This is a summary of the chat."

    def generate_pals(self, chats: List[Chat]) -> str:
        return "Here are some generated PALs."

    def get_writing_suggestion(self, chats: List[Chat]) -> str:
        return "You can try writing about the following topics: topic1, topic2, topic3."