import numpy as np
from pysilsub import SpectralSensitivities, Stimuli


def compute_photoreceptor_excitation(image: np.ndarray) -> np.ndarray:
    """
    Compute photoreceptor excitations using pysilsub.

    Parameters:
        image: np.ndarray
            RGB image with values in [0,1].

    Returns:
        np.ndarray: Excitation map with shape (H, W, 4) for L, M, S cones, and rods.
    """
    ss = SpectralSensitivities(observer='CIE 2 Degree Standard Observer')
    height, width, _ = image.shape
    excitations = np.zeros((height, width, 4))
    for x in range(height):
        for y in range(width):
            r, g, b = image[x, y]
            stim = Stimuli({'R': r, 'G': g, 'B': b})
            try:
                excitations[x, y] = ss.get_response(stim)
            except AttributeError:
                excitations[x, y] = ss.get_excitations(stim)
    return excitations
