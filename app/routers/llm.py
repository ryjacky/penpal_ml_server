from typing import List, Annotated

from modules.auth.authorization import validate_session_with_supabase
from modules.llm.llm_client import LLMClient
from modules.llm.prototype_llm_client import PrototypeLLMClient
from modules.llm.types import Chat, ChatSummary, Pal, WritingSuggestion
from fastapi import APIRouter, Depends
import clients as clients

llm_router = APIRouter(prefix="/llm")


@llm_router.post("/pals")
async def get_pals(
        prompt: str,
        credentials: Annotated[str, Depends(validate_session_with_supabase)]) -> List[Pal]:
    """
    Receives an essay prompt and returns an array of three character profiles based on the prompt.
    """
    return [clients.chat_client.generate_pals(prompt)]