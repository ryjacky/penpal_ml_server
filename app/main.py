# Building the FastAPI app
import asyncio
import threading
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from modules.worker.writing_worker import writing_worker
from modules.worker.chatbot_worker import chatbot_worker
from routers.ocr import ocr_router
from routers.llm import llm_router

def chatbot_worker_thread(*params):
    asyncio.run(chatbot_worker())

def writing_worker_thread(*params):
    asyncio.run(writing_worker())


t = threading.Thread(target=chatbot_worker_thread, daemon=True)
t.start()
t = threading.Thread(target=writing_worker_thread, daemon=True)
t.start()

app = FastAPI()
app.include_router(llm_router)
app.include_router(ocr_router)