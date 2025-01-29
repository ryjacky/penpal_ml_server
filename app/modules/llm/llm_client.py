import json
import os
from abc import ABC, abstractmethod
from typing import List

from modules.llm.types import Chat


class LLMClient(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_chat_response(self, chats: List[Chat]) -> str:
        pass

    @abstractmethod
    def summarize_chat(self, chats: List[Chat]) -> str:
        pass

    @abstractmethod
    def generate_pals(self, chats: List[Chat]) -> str:
        pass

    @abstractmethod
    def get_writing_suggestion(self, chats: List[Chat]) -> str:
        pass