import json
import os
from abc import ABC, abstractmethod
from typing import List
from PIL import Image
from app.modules.ocr.ocr_client import OCRClient


class PrototypeOCRClient(OCRClient):
    def __init__(self, model_path: str, n_gpu_layers: int = -1):
        super().__init__(model_path, n_gpu_layers)

    def extract_writing(self, image: Image) -> str:
        # Hardcoded output
        return "This is a hardcoded text extracted from the image."