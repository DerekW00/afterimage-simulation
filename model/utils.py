import cv2
import numpy as np


def read_image_grayscale(path: str) -> np.ndarray:
    """
    Read an image from a file path in grayscale.

    Parameters
    ----------
    path : str
        Path to the image file.

    Returns
    -------
    np.ndarray
        Grayscale image.
    """
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Image not found at: {path}")
    return image

def read_image_color(path: str) -> np.ndarray:
    """Reads an image in color (BGR)."""
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(f"Image not found: {path}")
    return img / 255.0  # Normalize to [0, 1]


def save_image(path: str, image: np.ndarray):
    """
    Save an image to a specified file path.

    Parameters
    ----------
    path : str
        Destination file path.
    image : np.ndarray
        Image array to save.
    """
    cv2.imwrite(path, image)
