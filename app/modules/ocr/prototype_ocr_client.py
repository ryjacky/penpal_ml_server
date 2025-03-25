import json
import os
from abc import ABC, abstractmethod
from typing import List
from PIL import Image
from modules.ocr.ocr_client import OCRClient


class PrototypeOCRClient(OCRClient):
    def __init__(self):
        pass

    def extract_writing(self, url: str) -> str:
        # Hardcoded output
        return "This is a hardcoded text extracted from the image."