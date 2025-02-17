import numpy as np
from model.receptor_kinetics import update_opsin_concentration


def simulate_photoreceptor_response(hdr_radiance: np.ndarray, params: dict) -> np.ndarray:
    """
    Simulate the photoreceptor (rod/cone) response from an HDR radiance map.

    Parameters
    ----------
    hdr_radiance : np.ndarray
        HDR radiance map (float values).
    params : dict
        Dictionary of parameters:
          - ca: activation constant (default: 0.3)
          - cd: deactivation constant (default: 0.3)
          - dt: time step (default: 0.032)
          - iterations: number of simulation steps (default: 10)

    Returns
    -------
    np.ndarray
        Simulated photoreceptor response (e.g., opsin concentration map).
    """
    # Initialize with full opsin concentration (r=1)
    r = np.ones_like(hdr_radiance)
    ca = params.get('ca', 0.3)
    cd = params.get('cd', 0.3)
    dt = params.get('dt', 0.032)
    iterations = params.get('iterations', 10)

    for _ in range(iterations):
        r = update_opsin_concentration(r, hdr_radiance, ca=ca, cd=cd, dt=dt)

    return r
