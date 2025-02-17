import numpy as np

from model.model_config import ModelConfig
from model.utils.pysilsub_integration import compute_photoreceptor_excitation


def simulate_spectral_temporal_bleaching(image: np.ndarray, initial_state: np.ndarray = None,
                                         dt: float = None, iterations: int = None) -> np.ndarray:
    """
    Simulate the spectral temporal bleaching of photoreceptors using PySilSub.

    Parameters:
        image: np.ndarray
            Input RGB image with values in [0, 1].
        initial_state: np.ndarray, optional
            Initial opsin state; if None, defaults to ones.
        dt: float, optional
            Time step (defaults to ModelConfig.TIME_STEP).
        iterations: int, optional
            Number of iterations (defaults to ModelConfig.ITERATIONS).

    Returns:
        np.ndarray: Final opsin state with shape (H, W, 4) (for L, M, S cones, and rods).
    """
    if dt is None:
        dt = ModelConfig.TIME_STEP
    if iterations is None:
        iterations = ModelConfig.ITERATIONS

    # Get excitations from PySilSub
    excitations = compute_photoreceptor_excitation(image)
    # Initialize state if not provided (full sensitivity)
    if initial_state is None:
        initial_state = np.ones_like(excitations)

    ca = np.array(ModelConfig.CA_PS)  # shape (4,)
    cd = np.array(ModelConfig.CD_PS)  # shape (4,)

    state = initial_state
    for _ in range(iterations):
        dstate_dt = ca * excitations * (1 - state) - cd * state
        state = state + dt * dstate_dt
        state = np.clip(state, 0, 1)
    return state
