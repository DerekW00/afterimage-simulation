import os

import cv2
import numpy as np

from model.model_config import ModelConfig


def read_image(path: str = None, color: bool = True) -> np.ndarray:
    """
    Read an image (color or grayscale) and normalize to [0,1]. Uses default path if None.
    """
    if path is None:
        path = ModelConfig.DEFAULT_INPUT_DIR
    flag = cv2.IMREAD_COLOR if color else cv2.IMREAD_GRAYSCALE
    img = cv2.imread(path, flag)
    if img is None:
        raise FileNotFoundError(f"Image not found: {path}")
    if color:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img / 255.0


def save_image(path: str, image: np.ndarray) -> None:
    """
    Save an image (assumed RGB with values [0,1]). Uses default output directory if path not fully specified.
    """
    # If no directory provided, use default output
    directory = os.path.dirname(path)
    if not directory:
        directory = ModelConfig.DEFAULT_OUTPUT_DIR
        path = os.path.join(directory, path)
    os.makedirs(directory, exist_ok=True)
    image_to_save = (image * 255).astype(np.uint8)
    if image_to_save.ndim == 3 and image_to_save.shape[2] == 3:
        image_to_save = cv2.cvtColor(image_to_save, cv2.COLOR_RGB2BGR)
    cv2.imwrite(path, image_to_save)


def list_images(folder: str = None) -> list:
    """
    Return a sorted list of image filenames in the given folder. Uses default input folder if None.
    """
    if folder is None:
        folder = ModelConfig.DEFAULT_INPUT_DIR
    return sorted([f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.png'))])
