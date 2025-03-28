import json
import os
from abc import ABC, abstractmethod
from typing import List
from PIL import Image
from modules.ocr.ocr_client import OCRClient
from openai import OpenAI


class VllmOCRClient(OCRClient):
    def __init__(self):
        super().__init__()
        base_url = os.environ.get("OCR_SERVER_URL")
        self.client = OpenAI(
            base_url=base_url,
            api_key="token-abc123",

        )

        self.model_name = "fyp-penpal-ocr"

    def extract_writing(self, url: str) -> str | None:
        try:
            chat_response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": """You are a high accuracy OCR model that smartly transcribe the needed parts of a document according to the given instruction.
    You will be provided several scans of a student's *writing passage* to a writing prompt. Your goal is to extract *only* the student's written or typed response to the writing prompt, ignoring all other text or elements on the page.
    
    You output in the following format:
    ```
    The student's writing that is extracted from the images:
    ---
    <The transcribed text>
    ```
    """},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Here are the scans of a student's written or typed passage."},
                        {"type": "image_url", "image_url": {"url": url}},
                    ],
                }],
            )
            return chat_response.choices[0].message.content
        except:
            print("VLLM OCR Client ERROR: Cannot communicate with the inference server")