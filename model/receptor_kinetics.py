import numpy as np


def update_opsin_concentration(current_r: np.ndarray, effective_radiance: np.ndarray,
                               ca: float = 0.3, cd: float = 0.3, dt: float = 0.032) -> np.ndarray:
    """
    Update the opsin concentration based on a simple bleaching/regeneration model.

    The model follows:
        dr/dt = ca * effective_radiance * (1 - r) - cd * r

    Parameters
    ----------
    current_r : np.ndarray
        Current opsin concentration (values in [0, 1]).
    effective_radiance : np.ndarray
        Driving radiance signal.
    ca : float, optional
        Activation (bleaching) constant (default: 0.3).
    cd : float, optional
        Deactivation (regeneration) constant (default: 0.3).
    dt : float, optional
        Time step in seconds (default: 0.032).

    Returns
    -------
    np.ndarray
        Updated opsin concentration, clamped to [0, 1].
    """
    dr_dt = ca * effective_radiance * (1 - current_r) - cd * current_r
    new_r = current_r + dt * dr_dt
    return np.clip(new_r, 0, 1)
