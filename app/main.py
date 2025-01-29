# Building the FastAPI app
from fastapi import FastAPI

from routers.ocr import ocr_router
from routers.llm import llm_router
app = FastAPI()
app.include_router(llm_router)
app.include_router(ocr_router)