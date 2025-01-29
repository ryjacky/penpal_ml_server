import json
import os
from abc import ABC, abstractmethod
from typing import List
from PIL import Image

class OCRClient(ABC):
    def __init__(self):
        self.model_path = model_path
        self.n_gpu_layers = n_gpu_layers

    @abstractmethod
    def extract_writing(self, image: Image) -> str:
        pass