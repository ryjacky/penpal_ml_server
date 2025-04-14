import base64
import tempfile
from typing import List
import requests
from PIL.Image import Image
from google import genai
from google.genai import types
from .ocr_client import OCRClient
import os

class GeminiOCRClient(OCRClient):
    def __init__(self):
        super().__init__()

    def extract_writing(self, images: List[Image], writing_prompt: str) -> str:
        img_ids: list[str] = []
        for image in images:
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
                image.save(temp_file.name, format="JPEG")
                temp_file_path = temp_file.name
                
            response = self.upload_image(user_id="abc-123", file_path=temp_file_path)
            img_ids.append(response.get("id"))
            os.remove(temp_file_path)

        self.generate(img_ids, writing_prompt)

    def generate(self, img_ids: List[str], writing_prompt: str) -> str:
        headers = {
            'Authorization': 'Bearer {api_key}',
            'Content-Type': 'application/json',
        }

        files: list[dict[str,str]] = []
        for img_id in img_ids:
            files.append({
                'type': 'image',
                'transfer_method': 'local_file',
                'upload_file_id': img_id,
            })
        json_data = {
            'inputs': {"writing_prompt": writing_prompt},
            'query': '<NOT RELATED NOT USED>',
            'response_mode': 'blocking',
            'conversation_id': '',
            'user': 'abc-123',
            'files': [
                files
            ],
        }

        response = requests.post('https://api.dify.ai/v1/chat-messages', headers=headers, json=json_data)
        print(response.content.decode('utf-8'))

    def upload_image(self, user_id: str, file_path: str):
        """
        Uploads an image to the Dify API.

        Args:
            api_key (str): The API key for authentication.
            file_path (str): The local file path of the image to upload.
            user_id (str): The user ID to associate with the upload.

        Returns:
            dict: The response from the API.
        """
        url = "https://api.dify.ai/v1/files/upload"
        headers = {
            "Authorization": f"Bearer {os.getenv('DIFY_KEY')}",
        }
        files = {
            "file": (file_path, open(file_path, "rb"), "image/jpeg"),
            "user": (None, user_id)
        }

        response = requests.post(url, headers=headers, files=files)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()