import numpy as np
from pysilsub.observers import ColorimetricObserver
from pysilsub.problems import SilentSubstitutionProblem


def compute_photoreceptor_excitation(image: np.ndarray) -> np.ndarray:
    """
    Compute photoreceptor excitations using pysilsub.

    Parameters:
        image: np.ndarray
            RGB image with values in [0, 1].

    Returns:
        np.ndarray: Excitation map with shape (H, W, N) for N photoreceptor classes.
    """
    # Initialize observer and problem
    observer = ColorimetricObserver(age=32, field_size=10)
    ssp = SilentSubstitutionProblem.from_package_data('STLAB_1_York')
    ssp.observer = observer

    # Ensure all photoreceptors are accounted for before setting target_contrast
    ssp.ignore = ['rh']  # Ignore rods
    ssp.silence = ['mc', 'lc']  # Silence M and L cones
    ssp.target = ['sc']  # Target S cones

    # Now it's safe to set the target contrast
    ssp.target_contrast = 0.2
    ssp.background = [0.5] * ssp.nprimaries  # Set uniform background

    # Prepare output array
    height, width, _ = image.shape
    excitations = np.zeros((height, width, len(ssp.observer.photoreceptors)))

    # Compute excitations
    for x in range(height):
        for y in range(width):
            try:
                solution = ssp.linalg_solve()  # No arguments passed
                excitations[x, y] = solution
            except Exception as e:
                print(f"Failed to compute excitation for pixel ({x},{y}): {e}")
                excitations[x, y] = np.zeros(len(ssp.observer.photoreceptors))

    return excitations
