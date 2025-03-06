from io import BytesIO

import cv2
import numpy as np
from PIL import Image, ImageOps


def pre_process_image(img_bytes: bytes) -> Image:
    img = Image.open(BytesIO(img_bytes))
    img = np.array(img)

    # Normally, people include binarization in preprocessing, but we'll skip it as it is creating noises and
    # making text detection less accurate
    img = scale_down(img)
    img = np.array(img)
    img = normalize_image(img)
    img = grayscale_image(img)
    img = remove_noise(img, False)

    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


def scale_down(image: np.array) -> Image:
    """Scales an image to fit within a specific width and height while maintaining aspect ratio using OpenCV.

        Args:
            image (numpy.ndarray): The input image as a NumPy array.

        Returns:
            numpy.ndarray: The scaled image as a NumPy array.
        """


    img = Image.fromarray(image)

    return ImageOps.contain(img, (720, 720))


def normalize_image(img: np.array) -> Image:
    """
    Normalizes the input image by rescaling the pixel values to the range [0, 255].

    Parameters:
        img (np.array): The input image as a NumPy array.

    Returns:
        Image: The normalized image as a NumPy array.
    """
    norm_img = np.zeros((img.shape[0], img.shape[1]))
    img = cv2.normalize(img, norm_img, 0, 255, cv2.NORM_MINMAX)

    return img


def grayscale_image(img: Image) -> Image:
    """
    Converts an RGB image to grayscale and then converts it back to RGB mode.

    Args:
        img (Image): The input image to be converted to grayscale.

    Returns:
        Image: The grayscale image in RGB mode.
    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    return img


def remove_noise(image, colored=True):
    if colored:
        image = cv2.fastNlMeansDenoisingColored(image, None, 5, 10, 7, 15)
    else:
        image = cv2.fastNlMeansDenoising(image, None, 5, 7, 15)
    return image