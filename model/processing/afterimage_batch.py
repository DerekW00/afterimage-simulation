import os

import numpy as np

from model.core.receptor_kinetics import update_opsin_concentration
from model.model_config import ModelConfig
from model.utils.file_utils import read_image, save_image, list_images


def process_frame_sequence(input_folder: str = None, output_folder: str = None):
    if input_folder is None:
        input_folder = ModelConfig.DEFAULT_INPUT_DIR
    if output_folder is None:
        output_folder = ModelConfig.DEFAULT_OUTPUT_DIR

    os.makedirs(output_folder, exist_ok=True)
    files = list_images(input_folder)
    if not files:
        print("No frames found!")
        return

    opsin = None
    for i, fname in enumerate(files):
        input_path = os.path.join(input_folder, fname)
        output_path = os.path.join(output_folder, fname)
        frame = read_image(input_path, color=True)
        if opsin is None:
            opsin = np.ones_like(frame)
        for _ in range(ModelConfig.ITERATIONS):
            opsin = update_opsin_concentration(opsin, frame)
        # afterimage = (1.0 - opsin.mean(axis=2)) * ModelConfig.INTENSITY
        # afterimage = np.clip(afterimage, 0, 1)
        # afterimage_rgb = np.stack([afterimage] * 3, axis=-1)
        afterimage = 1.0 - opsin  # This preserves per-channel bleaching
        afterimage *= ModelConfig.INTENSITY
        afterimage = np.clip(afterimage, 0, 1)
        save_image(output_path, afterimage)
        print(f"Processed frame {i + 1}/{len(files)}")
    print("Batch processing completed.")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Batch process frames to add afterimage effects.")
    parser.add_argument("--input_folder", default=None, help="Input folder (default: ModelConfig.DEFAULT_INPUT_DIR)")
    parser.add_argument("--output_folder", default=None, help="Output folder (default: ModelConfig.DEFAULT_OUTPUT_DIR)")
    args = parser.parse_args()
    process_frame_sequence(args.input_folder, args.output_folder)


if __name__ == "__main__":
    main()
