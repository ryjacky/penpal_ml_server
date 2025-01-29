import json
import os
from abc import ABC, abstractmethod
from typing import List

from llm.types import Chat


class LLMClient(ABC):
    def __init__(self, model_path: str, n_gpu_layers: int = -1):
        self.model_path = model_path
        self.n_gpu_layers = n_gpu_layers

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