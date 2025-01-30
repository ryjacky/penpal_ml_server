# Building the FastAPI app
import asyncio
from fastapi import FastAPI

from modules.worker.chatbot_worker import chatbot_worker
from routers.ocr import ocr_router
from routers.llm import llm_router
app = FastAPI()
app.include_router(llm_router)
app.include_router(ocr_router)

asyncio.run(chatbot_worker())