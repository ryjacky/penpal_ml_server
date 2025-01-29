from typing import List
from app.modules.llm.llm_client import Endpoints
from app.modules.llm.types import Chat


class PrototypeLLMClient(Endpoints):
    def __init__(self, model_path: str, n_gpu_layers: int = -1):
        super().__init__(model_path, n_gpu_layers)

    def get_chat_response(self, chats: List[Chat]) -> str:
        return "This is a hardcoded chat response."

    def summarize_chat(self, chats: List[Chat]) -> str:
        return "This is a summary of the chat."

    def generate_pals(self, chats: List[Chat]) -> str:
        return "Here are some generated PALs."

    def get_writing_suggestion(self, chats: List[Chat]) -> str:
        return "You can try writing about the following topics: topic1, topic2, topic3."