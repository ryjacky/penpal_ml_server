import random
import string
import time
from typing import List
import requests
from PIL.Image import Image
from .ocr_client import OCRClient
import os

class GeminiOCRClient(OCRClient):
    def __init__(self):
        super().__init__()
        os.environ["DIFY_KEY"]= ""

    def extract_writing(self, images: List[Image], writing_prompt: str) -> str:
        img_ids: list[str] = []
        api_key = os.getenv("DIFY_KEY")

        for image in images:
            image.save("hi.jpg", format="JPEG")
            response = self.upload_file_to_dify("hi.jpg", "abc-123", api_key)
            print(response)
            os.remove("hi.jpg")
            img_ids.append(response.get("id"))

        self.generate(img_ids, writing_prompt, api_key)

    def generate(self, img_ids: list[str], writing_prompt: str, api_key) -> str:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        }

        json_data = {
            'inputs': {"writing_prompt": writing_prompt},
            'query': 'What are the specs of the iPhone 13 Pro Max?',
            'response_mode': 'blocking',
            'conversation_id': '',
            'user': 'abc-123',
            'files': [
                {
                    'type': 'image',
                    'transfer_method': 'local',
                    'upload_file_id': img_id,
                } for img_id in img_ids
            ],
        }

        response = requests.post('https://api.dify.ai/v1/chat-messages', headers=headers, json=json_data)
        writing = response.json()["answer"].split("---")[-1].strip()
        print(writing)
        return writing



    def upload_file_to_dify(self, file_path, user, api_key):
        headers = {
            'Authorization': f'Bearer {api_key}',
        }

        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        files = {
            'file': (f'{filename}.jpg', open(file_path, 'rb'), 'image/jpeg'),
            'user': (None, user),
        }

        response = requests.post('https://api.dify.ai/v1/files/upload', headers=headers, files=files)
        return response.json()