import numpy as np


def get_cone_density_map(image_shape: tuple, fovea_center: tuple, fovea_radius: float) -> np.ndarray:
    """
    Generate a normalized cone density map with peak density at the fovea.
    """
    height, width = image_shape
    Y, X = np.indices((height, width))
    dist = np.sqrt((X - fovea_center[0]) ** 2 + (Y - fovea_center[1]) ** 2)
    sigma = fovea_radius / 2.0
    density = np.exp(-0.5 * (dist / sigma) ** 2)
    return density / np.max(density)


def apply_anatomical_constraints(effective_radiance: np.ndarray, density_map: np.ndarray) -> np.ndarray:
    """
    Modulate effective radiance by cone density.
    """
    return effective_radiance * density_map
