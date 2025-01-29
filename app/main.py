# Building the FastAPI app
from fastapi import FastAPI

from app.routers.llm import llm_router
from app.routers.ocr import ocr_router
app = FastAPI()
app.include_router(llm_router)
app.include_router(ocr_router)