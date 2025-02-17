import numpy as np
import cv2
from model.receptor_kinetics import update_opsin_concentration

def generate_afterimage(input_image: np.ndarray, params: dict) -> np.ndarray:
    """
    Generate an afterimage from the input image by simulating photoreceptor bleaching.

    Parameters
    ----------
    input_image : np.ndarray
        Input image as a NumPy array (grayscale or single channel).
    params : dict
        Dictionary of parameters. Expected keys include:
          - intensity: scaling factor for the afterimage intensity (default: 1.0)
          - ca: activation constant (default: 0.3)
          - cd: deactivation constant (default: 0.3)
          - dt: time step in seconds (default: 0.032)
          - iterations: number of iterations to simulate (default: 10)

    Returns
    -------
    np.ndarray
        Processed image representing the afterimage (8-bit).
    """
    # Ensure the image is float32
    if input_image.dtype != np.float32:
        input_image = input_image.astype(np.float32) / 255.0

    # Clamp image values to [0,1]
    input_image = np.clip(input_image, 0, 1)

    # Initialize opsin concentration
    opsin = np.ones_like(input_image)

    ca = params.get('ca', 0.3)
    cd = params.get('cd', 0.3)
    dt = params.get('dt', 0.032)
    iterations = params.get('iterations', 10)

    # Simulate bleaching over time
    for _ in range(iterations):
        opsin = update_opsin_concentration(opsin, input_image, ca=ca, cd=cd, dt=dt)

    # Compute afterimage by subtracting from initial opsin state
    afterimage = 1.0 - opsin

    # Apply intensity factor
    afterimage *= params.get('intensity', 1.0)

    # Clip to [0, 1]
    afterimage = np.clip(afterimage, 0, 1)

    # Convert back to 8-bit
    result = (afterimage * 255).astype(np.uint8)
    return result


if __name__ == '__main__':
    import argparse
    from model.utils import read_image_grayscale, save_image

    parser = argparse.ArgumentParser(description="Generate an afterimage from an input image.")
    parser.add_argument("input_image", help="Path to the input image")
    parser.add_argument("output_image", help="Path to save the afterimage")
    args = parser.parse_args()

    # Load the input image
    image = read_image_grayscale(args.input_image)

    # Generate the afterimage
    params = {'intensity': 2.0, 'ca': 0.4, 'cd': 0.2, 'dt': 0.05, 'iterations': 20}
    result = generate_afterimage(image, params)

    # Save and display the result
    save_image(args.output_image, result)

    print("Afterimage saved to:", args.output_image)
