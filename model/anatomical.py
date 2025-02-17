# photoreceptor_model/anatomical.py

import numpy as np


def get_cone_density_map(image_shape: tuple, fovea_center: tuple, fovea_radius: float) -> np.ndarray:
    """
    Generate a spatial cone density map, with peak density at the fovea.

    Parameters
    ----------
    image_shape : tuple
        (height, width) of the simulated retinal map.
    fovea_center : tuple
        (x, y) coordinates of the fovea center.
    fovea_radius : float
        Radius (in pixels) defining the high-density foveal region.

    Returns
    -------
    np.ndarray
        Normalized density map (values between 0 and 1).
    """
    height, width = image_shape
    Y, X = np.indices((height, width))
    dist = np.sqrt((X - fovea_center[0]) ** 2 + (Y - fovea_center[1]) ** 2)

    # A Gaussian profile approximates high cone density in the fovea.
    sigma = fovea_radius / 2.0
    density = np.exp(-0.5 * (dist / sigma) ** 2)
    density = density / np.max(density)
    return density


def apply_anatomical_constraints(effective_radiance: np.ndarray, density_map: np.ndarray) -> np.ndarray:
    """
    Adjust the effective radiance by anatomical constraints (e.g., modulate by cone density).

    Parameters
    ----------
    effective_radiance : np.ndarray
        The effective radiance map.
    density_map : np.ndarray
        Normalized cone density map.

    Returns
    -------
    np.ndarray
        Anatomically adjusted radiance map.
    """
    return effective_radiance * density_map
