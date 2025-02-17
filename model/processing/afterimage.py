import numpy as np

from model.core.photoreceptor_model import simulate_spectral_temporal_bleaching
from model.model_config import ModelConfig
from model.utils.file_utils import read_image, save_image


def generate_afterimage_with_spectral_bleaching(input_image: np.ndarray, params: dict) -> np.ndarray:
    """
    Generate a colored afterimage using spectral temporal bleaching.

    Parameters:
        input_image: np.ndarray (RGB, [0,1])
        params: dict with keys 'intensity' and 'iterations'

    Returns:
        np.ndarray: Color afterimage in RGB, [0,1]
    """
    # Simulate the temporal bleaching using spectral excitations
    final_state = simulate_spectral_temporal_bleaching(
        input_image,
        iterations=params.get('iterations', ModelConfig.ITERATIONS)
    )
    # Assume final_state has shape (H, W, 4); use only the cone channels (first 3) for color
    opsin_cones = final_state[:, :, :3]
    # Compute complementary response for afterimage (simple inversion)
    afterimage = 1.0 - opsin_cones
    afterimage *= params.get('intensity', ModelConfig.INTENSITY)
    return np.clip(afterimage, 0, 1)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate an afterimage using spectral temporal bleaching.")
    parser.add_argument("input_image", help="Path to the input image")
    parser.add_argument("output_image", help="Path to save the afterimage")
    args = parser.parse_args()

    input_img = read_image(args.input_image, color=True)
    params = {'intensity': 2.0, 'iterations': 20}
    output_img = generate_afterimage_with_spectral_bleaching(input_img, params)
    save_image(args.output_image, output_img)
    print("Afterimage saved to:", args.output_image)


if __name__ == "__main__":
    main()
