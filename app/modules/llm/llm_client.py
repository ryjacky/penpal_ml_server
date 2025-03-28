import json
import os
from abc import ABC, abstractmethod
from typing import List

from modules.llm.types import Chat
from modules.llm.types import Pal


class LLMClient(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_chat_response(self, chats: List[Chat], bot_name: str, bot_bg: str, writing_prompt: str) -> str | None:
        pass

    @abstractmethod
    def summarize_chat(self, chats: List[Chat], bot_name: str) -> str | None:
        pass

    @abstractmethod
    def generate_pals(self, prompt: str) -> Pal | None:
        pass

    @abstractmethod
    def get_language_suggestion(self, writing: str, writing_prompt: str) -> str | None:
        pass

    @abstractmethod
    def get_content_suggestion(self, writing: str, writing_prompt: str) -> str | None:
        pass

    @abstractmethod
    def get_organization_suggestion(self, writing: str, writing_prompt: str) -> str | None:
        pass