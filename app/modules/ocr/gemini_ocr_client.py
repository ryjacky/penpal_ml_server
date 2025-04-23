import random
import string
import time
from typing import List
import requests
from PIL.Image import Image
from .ocr_client import OCRClient
import os
from io import BytesIO

from google import genai
from google.genai import types
import base64

class GeminiOCRClient(OCRClient):
    def __init__(self):
        super().__init__()
        self.prompt = "Extract the text from the image. If the text contains a student writing, please extract the writing and ignore the rest. The writing is in English. The image may contain some noise, but the text is clear. Please do not include any other information in your response. Just return the extracted text."
        self.prompt = os.getenv("GEMINI_PROMPT", self.prompt)

    def to_base64(self, image: Image) -> bytes:

        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = buffered.getvalue()
        return img_str
    
    def extract_writing(self, images: list[Image], writing_prompt: str) -> str:

        img_parts = []
        for image in images:
            img_parts.append(  types.Part.from_bytes(
                data=self.to_base64(image),
                      mime_type="image/jpeg",

                )
            )
        return self.generate(img_parts)


    def generate(self, images):
        client = genai.Client(
            vertexai=True,
            project="profound-jet-453603-h0",
            location="us-central1",
        )

        model = "gemini-2.0-flash-001"
        contents = [
            types.Content(
            role="user",
            parts=[
                  types.Part.from_text(text=self.prompt)
            ] + images
            )
        ]
        generate_content_config = types.GenerateContentConfig(
            temperature = 1,
            top_p = 0.95,
            max_output_tokens = 8192,
            response_modalities = ["TEXT"],
            speech_config = types.SpeechConfig(
            voice_config = types.VoiceConfig(
                prebuilt_voice_config = types.PrebuiltVoiceConfig(
                voice_name = "zephyr"
                )
            ),
            ),
            safety_settings = [types.SafetySetting(
            category="HARM_CATEGORY_HATE_SPEECH",
            threshold="OFF"
            ),types.SafetySetting(
            category="HARM_CATEGORY_DANGEROUS_CONTENT",
            threshold="OFF"
            ),types.SafetySetting(
            category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
            threshold="OFF"
            ),types.SafetySetting(
            category="HARM_CATEGORY_HARASSMENT",
            threshold="OFF"
            )],
        )

        response = ""
        for chunk in client.models.generate_content_stream(
            model = model,
            contents = contents,
            config = generate_content_config,
            ):
            response += chunk.text

        return response
