import os
import unittest
from io import BytesIO

import cv2
import numpy as np
from PIL import Image, ImageChops

from app.modules.ocr.preprocessing import pre_process_image, normalize_image, grayscale_image


class PreprocessingTestCase(unittest.TestCase):
    def setUp(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))

        self.test_image_path = os.path.join(self.dir_path, 'test.jpg')
        with open(self.test_image_path, 'rb') as f:
            self.test_image_bytes = f.read()

    def test_pre_process_image(self):
        img = pre_process_image(self.test_image_bytes)
        expected = Image.open(os.path.join(self.dir_path, 'test_pre_process_image_verify.jpg'))
        diff = ImageChops.difference(img, expected)

        self.assertEqual(diff.getbbox() is not None, True)

    def test_normalize_image(self):
        img = Image.open(BytesIO(self.test_image_bytes))
        img = np.array(img)
        img = normalize_image(img)
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        expected = Image.open(os.path.join(self.dir_path, 'test_normalize_image_verify.jpg'))
        diff = ImageChops.difference(img, expected)

        self.assertEqual(diff.getbbox() is not None, True)

    def test_grayscale_image(self):
        img = Image.open(BytesIO(self.test_image_bytes))
        img = np.array(img)
        img = grayscale_image(img)
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        expected = Image.open(os.path.join(self.dir_path, 'test_grayscale_image_verify.jpg'))
        diff = ImageChops.difference(img, expected)

        self.assertEqual(diff.getbbox() is not None, True)


if __name__ == '__main__':
    unittest.main()
