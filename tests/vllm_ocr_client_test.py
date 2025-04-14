import unittest
import os
from unittest.mock import patch, MagicMock
from PIL import Image
from app.modules.ocr.vllm_ocr_client import VllmOCRClient

class TestVllmOCRClientIntegration(unittest.TestCase):
    def setUp(self):
        # Set up the environment variables needed for the test
        os.environ["OCR_SERVER_URL"] = "https://api.openai.com/v1"

    def test_extract_writing(self):
        # Create a test image
        image = Image.new('RGB', (100, 100))

        # Create a VllmOCRClient instance
        client = VllmOCRClient()

        # Call the extract_writing method
        result = client.extract_writing(image)

        # Assert that the result is not empty
        self.assertIsNotNone(result)

        # Assert that the result is a string
        self.assertIsInstance(result, str)

if __name__ == '__main__':
    unittest.main()