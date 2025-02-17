import cv2
import numpy as np


def load_hdr_image(path: str) -> np.ndarray:
    """
    Load an HDR image as a floating-point array.
    """
    hdr = cv2.imread(path, -1)
    if hdr is None:
        raise FileNotFoundError(f"HDR image not found: {path}")
    return hdr


def convert_to_effective_radiance(hdr_image: np.ndarray, exposure: float = 1.0) -> np.ndarray:
    """
    Scale HDR image with an exposure factor.
    """
    return hdr_image * exposure
