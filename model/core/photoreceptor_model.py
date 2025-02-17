import numpy as np

from model.utils.pysilsub_integration import compute_photoreceptor_excitation


def simulate_photoreceptor_response(image: np.ndarray) -> np.ndarray:
    """
    Simulate photoreceptor responses for an input image.

    Parameters:
        image: np.ndarray
            RGB image with values in [0,1].

    Returns:
        np.ndarray: Photoreceptor excitation map.
    """
    return compute_photoreceptor_excitation(image)
