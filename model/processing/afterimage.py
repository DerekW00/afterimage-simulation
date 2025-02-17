import numpy as np

from model.core.receptor_kinetics import update_opsin_concentration
from model.utils.file_utils import save_image


def generate_afterimage(input_image: np.ndarray, params: dict) -> np.ndarray:
    """
    Generate an afterimage from a single input image.
    """
    opsin = np.ones_like(input_image)
    iterations = params.get('iterations', 20)
    for _ in range(iterations):
        opsin = update_opsin_concentration(opsin, input_image)
    afterimage = (1.0 - opsin.mean(axis=2)) * params.get('intensity', 2.0)
    return np.clip(afterimage, 0, 1)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate an afterimage from a single image.")
    parser.add_argument("input_image", nargs='?', default=None,
                        help="Input image path (default: use data/afterimage/0_1_frame_prototype/input/frame_0000.jpg)")
    parser.add_argument("output_image", nargs='?', default=None,
                        help="Output image path (default: use data/afterimage/0_1_frame_prototype/output/frame_0000.jpg)")
    args = parser.parse_args()

    from model.utils.file_utils import read_image
    input_img = read_image(args.input_image, color=True)
    params = {'intensity': 2.0, 'iterations': 20}
    output_img = generate_afterimage(input_img, params)
    output_img_rgb = np.stack([output_img] * 3, axis=-1)
    save_image(args.output_image, output_img_rgb)
    print("Afterimage generated and saved.")


if __name__ == "__main__":
    main()
