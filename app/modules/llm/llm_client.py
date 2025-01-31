import json
import os
from abc import ABC, abstractmethod
from typing import List, Literal

from modules.llm.types import Chat


class LLMClient(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_chat_response(self, chats: List[Chat], name: str, background: str, writing_prompt: str) -> str:
        pass

    @abstractmethod
    def summarize_chat(self, chats: List[Chat]) -> str:
        pass

    @abstractmethod
    def generate_pals(self, essay_prompt: str) -> str:
        pass

    @abstractmethod
    def get_writing_suggestion(
            self,
            writing: str,
            grading_aspect: Literal["language", "organization", "content"],
            ) -> str:        
        pass