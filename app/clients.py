import os

from supabase import create_client, Client

from modules.llm.vllm_client import VLLMClient
from modules.llm.llm_client import LLMClient
from modules.llm.prototype_llm_client import PrototypeLLMClient

supabase_client: Client = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

mode = os.getenv("MODE")

if mode == "VLLM":
    chat_client: LLMClient = VLLMClient()
else:
    chat_client: LLMClient = PrototypeLLMClient()