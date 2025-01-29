from PIL.Image import Image
import cv2
import numpy as np
from scipy.ndimage import gaussian_filter, label


class Dot:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)


class Segment:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = int(x1)
        self.y1 = int(y1)
        self.x2 = int(x2)
        self.y2 = int(y2)

    def center(self) -> Dot:
        return Dot(x=(self.x1 + self.x2) / 2, y=(self.y1 + self.y2) / 2)

    def area(self):
        return abs(self.x2 - self.x1) * abs(self.y2 - self.y1)


class ImageSegment(Segment):
    """
    Initializes the ImageSegment with the coordinates of the bounding box and the associated image.

    Parameters:
        x1 (int): The x-coordinate of the top-left corner.
        y1 (int): The y-coordinate of the top-left corner.
        x2 (int): The x-coordinate of the bottom-right corner.
        y2 (int): The y-coordinate of the bottom-right corner.
        image (Image): The associated image.

    Returns:
        None
    """

    def __init__(self, x1: int, y1: int, x2: int, y2: int, image: Image):
        super().__init__(x1, y1, x2, y2)
        self.image = image.crop((x1, y1, x2, y2))

    def weighted_center(self) -> Dot:
        """
        Calculates the weighted center of a connected component in an image. The weighted center
        is the center where the dark pixels aggregate the most.

        Returns:
            Dot: A Dot object representing the weighted center of the connected component.
        """
        image = np.array(self.image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 1. Smooth the image:
        smoothed_image = gaussian_filter(image, sigma=1)

        # 2. Apply Otsu's thresholding:
        _, thresholded_image = cv2.threshold(smoothed_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        thresholded_image = thresholded_image / 255  # Normalize to 0-1

        # 3. Label connected components:
        labels, num_features = label(thresholded_image)

        # 4. Find the largest connected component:
        largest_label = np.argmax(np.bincount(labels.flatten())[1:]) + 1

        # 5. Calculate the center:
        area_indices = np.where(labels == largest_label)
        center_row = np.mean(area_indices[0])
        center_col = np.mean(area_indices[1])

        return Dot(x=int(center_col + self.x1), y=int(center_row + self.y1))