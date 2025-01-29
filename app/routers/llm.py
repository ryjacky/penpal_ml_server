from typing import List, Annotated

from modules.auth.authorization import validate_session_with_supabase
from modules.llm.llm_client import LLMClient
from modules.llm.prototype_llm_client import PrototypeLLMClient
from modules.llm.types import Chat, ChatSummary, Pal
from fastapi import APIRouter, Depends

llm_router = APIRouter(prefix="/llm")
client: LLMClient = PrototypeLLMClient()

@llm_router.post("/reply")
def chat(
        chats: List[Chat],
        credentials: Annotated[str, Depends(validate_session_with_supabase)]) -> List[Chat]:
    """
    Receive a list of chat messages and return a list of chat messages with the bot's response.
    The last message in the list will be the bot's response.
    """
    return client.get_chat_response(chats)


@llm_router.post("/chat_summary")
async def summarize(
        chats: List[Chat],
        credentials: Annotated[str, Depends(validate_session_with_supabase)]) -> ChatSummary:
    """
    It receives a message in ChatML format and returns a response in ChatML format with a summary
     as the last bot message.
    """
    return client.summarize_chat(chats)


@llm_router.post("/pals")
async def get_pals(
        prompt: str,
        credentials: Annotated[str, Depends(validate_session_with_supabase)]) -> List[Pal]:
    """
    Receives an essay prompt and returns an array of three character profiles based on the prompt.
    """
    return client.get_pals(prompt)