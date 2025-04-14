import json
import os
from abc import ABC, abstractmethod
from typing import List
from PIL import Image

class OCRClient(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def extract_writing(self, images: list[Image]) -> str:
        pass