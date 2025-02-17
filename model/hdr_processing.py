import numpy as np
import cv2


def load_hdr_image(path: str) -> np.ndarray:
    """
    Load an HDR image from the specified path.

    Parameters
    ----------
    path : str
        File path to the HDR image.

    Returns
    -------
    np.ndarray
        HDR image as a floating-point array.
    """
    # Use cv2.IMREAD_ANYDEPTH flag (or -1) to load HDR images properly
    hdr = cv2.imread(path, -1)
    if hdr is None:
        raise FileNotFoundError(f"HDR image not found at: {path}")
    return hdr


def convert_to_effective_radiance(hdr_image: np.ndarray, exposure: float = 1.0) -> np.ndarray:
    """
    Convert an HDR image into an effective radiance map.

    Parameters
    ----------
    hdr_image : np.ndarray
        HDR image array.
    exposure : float, optional
        Exposure scaling factor (default is 1.0).

    Returns
    -------
    np.ndarray
        Effective radiance map.
    """
    effective_radiance = hdr_image * exposure
    return effective_radiance
