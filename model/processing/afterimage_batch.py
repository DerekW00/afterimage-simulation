import os

import cv2
import numpy as np

from model.core.receptor_kinetics import update_opsin_concentration
from model.model_config import ModelConfig
from model.utils.file_utils import read_image, save_image, list_images

# You can add a persistent overlay blending weight to your config, or define it here:
PERSISTENT_ALPHA = 0.5  # Weight for the previous frame's afterimage in the overlay


def process_frame_sequence(input_folder: str = None, output_folder: str = None):
    if input_folder is None:
        input_folder = ModelConfig.DEFAULT_INPUT_DIR
    if output_folder is None:
        output_folder = ModelConfig.DEFAULT_OUTPUT_DIR

    # Create output folders: one for the afterimage frames, one for persistent overlay frames.
    os.makedirs(output_folder, exist_ok=True)
    persistent_overlay_folder = os.path.join(output_folder, "persistent_overlay")
    os.makedirs(persistent_overlay_folder, exist_ok=True)

    files = list_images(input_folder)
    if not files:
        print("No frames found!")
        return

    # Initialize opsin for afterimage generation.
    opsin = None
    previous_afterimage = None  # For persistent overlay

    for i, fname in enumerate(files):
        input_path = os.path.join(input_folder, fname)
        output_path = os.path.join(output_folder, fname)
        overlay_path = os.path.join(persistent_overlay_folder, fname)

        frame = read_image(input_path, color=True)
        if frame is None:
            print(f"Skipping {fname} due to read error.")
            continue

        # If first frame, initialize opsin as ones (same shape as frame)
        if opsin is None:
            opsin = np.ones_like(frame)

        # Update opsin over several iterations to simulate bleaching.
        for _ in range(ModelConfig.ITERATIONS):
            opsin = update_opsin_concentration(opsin, frame)

        # Compute afterimage using per-channel processing.
        afterimage = 1.0 - opsin  # preserves color differences
        afterimage *= ModelConfig.INTENSITY
        afterimage = np.clip(afterimage, 0, 1)

        # Save the afterimage frame.
        save_image(output_path, afterimage)
        print(f"Processed frame {i + 1}/{len(files)} (afterimage saved)")

        # Create persistent overlay:
        # For the first frame, use the original.
        if i == 0:
            persistent_overlay = frame.copy()
        else:
            # Blend current original with previous frame's afterimage.
            # Note: cv2.addWeighted expects uint8 images.
            orig_uint8 = (frame * 255).astype(np.uint8)
            prev_af_uint8 = (previous_afterimage * 255).astype(np.uint8)
            persistent_overlay = cv2.addWeighted(orig_uint8, 1 - PERSISTENT_ALPHA, prev_af_uint8, PERSISTENT_ALPHA, 0)
            persistent_overlay = persistent_overlay.astype(np.float32) / 255.0

        # Save the persistent overlay frame.
        save_image(overlay_path, persistent_overlay)
        print(f"Persistent overlay frame saved: {overlay_path}")

        # Update previous_afterimage for next frame.
        previous_afterimage = afterimage.copy()

    print("Batch processing completed.")


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Batch process frames to generate afterimage and persistent overlay effects.")
    parser.add_argument("--input_folder", default=None, help="Input folder (default: ModelConfig.DEFAULT_INPUT_DIR)")
    parser.add_argument("--output_folder", default=None, help="Output folder (default: ModelConfig.DEFAULT_OUTPUT_DIR)")
    args = parser.parse_args()
    process_frame_sequence(args.input_folder, args.output_folder)


if __name__ == "__main__":
    main()
