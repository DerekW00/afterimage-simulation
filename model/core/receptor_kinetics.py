import numpy as np

from model.model_config import ModelConfig


def update_opsin_concentration(opsin: np.ndarray, radiance: np.ndarray) -> np.ndarray:
    """
    Update opsin concentration with color-dependent bleaching for each channel.

    Uses:
       dr/dt = ca * radiance * (1 - opsin) - cd * opsin

    Parameters:
        opsin : np.ndarray
            Current opsin concentration (H x W x 3 for RGB).
        radiance : np.ndarray
            Input radiance map (H x W x 3).
    Returns:
        np.ndarray: Updated opsin concentrations, clamped to [0, 1].
    """
    ca_rgb = ModelConfig.CA_RGB
    cd_rgb = ModelConfig.CD_RGB
    dt = ModelConfig.TIME_STEP

    dr_dt = np.zeros_like(opsin)
    for c in range(3):
        dr_dt[:, :, c] = ca_rgb[c] * radiance[:, :, c] * (1 - opsin[:, :, c]) - cd_rgb[c] * opsin[:, :, c]

    new_opsin = opsin + dt * dr_dt
    return np.clip(new_opsin, 0, 1)
