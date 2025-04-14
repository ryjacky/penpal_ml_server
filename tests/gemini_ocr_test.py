import unittest
from unittest.mock import patch, MagicMock
from PIL import Image
from app.modules.ocr.gemini_ocr_client import GeminiOCRClient


class TestGeminiOCRClient(unittest.TestCase):
    def setUp(self):
        # Initialize the GeminiOCRClient
        self.ocr_client = GeminiOCRClient()

    @patch("app.modules.ocr.gemini_ocr_client.genai.Client")
    def test_extract_writing(self, mock_genai_client):
        # Mock the genai.Client and its methods
        mock_client_instance = MagicMock()
        mock_genai_client.return_value = mock_client_instance
        mock_client_instance.models.generate_content_stream.return_value = [
            MagicMock(text="Extracted text from image 1"),
            MagicMock(text="Extracted text from image 2"),
        ]

        # Load the test image
        with Image.open("test/test.jpg") as img:
            images = [img]

            # Call the extract_writing method
            result = self.ocr_client.extract_writing(images)

        # Assert the result
        self.assertEqual(
            result,
            "Extracted text from image 1\nExtracted text from image 2",
        )

        # Verify that the API was called with the correct parameters
        mock_client_instance.models.generate_content_stream.assert_called()

    @patch("app.modules.ocr.gemini_ocr_client.base64.b64encode")
    def test_image_to_base64(self, mock_b64encode):
        # Mock the base64 encoding
        mock_b64encode.return_value = b"mock_base64_string"

        # Load the test image
        with Image.open("test/test.jpg") as img:
            result = self.ocr_client._image_to_base64(img)

        # Assert the result
        self.assertEqual(result, "mock_base64_string")


if __name__ == "__main__":
    unittest.main()