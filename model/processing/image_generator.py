import os

import cv2
import numpy as np

from model.model_config import ModelConfig


def generate_test_frames(output_dir=None, frame_count=30, image_size=(500, 500)):
    """
    Generate a sequence of synthetic, colored test frames.

    The generated frames include:
      - A two-dimensional gradient background.
      - A moving circle whose center moves in a sine/cosine pattern.
      - The circle’s color smoothly cycles through red, green, and blue.

    These frames provide rich color content for subsequent afterimage processing.

    Parameters:
        output_dir (str): Directory to save the frames.
                          Defaults to ModelConfig.DEFAULT_INPUT_DIR if not provided.
        frame_count (int): Number of frames to generate.
        image_size (tuple): Dimensions of each frame (height, width).
    """
    if output_dir is None:
        output_dir = ModelConfig.DEFAULT_INPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    height, width = image_size

    # Create a horizontal and vertical gradient background.
    x_grad = np.tile(np.linspace(0, 255, width, dtype=np.uint8), (height, 1))
    y_grad = np.tile(np.linspace(0, 255, height, dtype=np.uint8), (width, 1)).T
    # Construct a background: R from x gradient, G from y gradient, B as average.
    background = np.stack([
        x_grad,
        y_grad,
        ((x_grad.astype(np.uint16) + y_grad.astype(np.uint16)) // 2).astype(np.uint8)
    ], axis=2)

    # Loop to generate frames.
    for i in range(frame_count):
        # Start with a copy of the gradient background.
        frame = background.copy()

        # Calculate a moving circle center.
        center_x = int(width / 2 + (width / 3) * np.sin(2 * np.pi * i / frame_count))
        center_y = int(height / 2 + (height / 4) * np.cos(2 * np.pi * i / frame_count))
        radius = 50

        # Cycle through colors smoothly using sine functions.
        red = int(127 * (np.sin(2 * np.pi * i / frame_count) + 1))
        green = int(127 * (np.sin(2 * np.pi * i / frame_count + 2 * np.pi / 3) + 1))
        blue = int(127 * (np.sin(2 * np.pi * i / frame_count + 4 * np.pi / 3) + 1))
        # OpenCV uses BGR order.
        circle_color = (blue, green, red)

        cv2.circle(frame, (center_x, center_y), radius, circle_color, -1)

        # Optionally: you can add more elements here (e.g. additional shapes, noise, etc.)

        filename = os.path.join(output_dir, f"frame_{i:04d}.jpg")
        cv2.imwrite(filename, frame)
        print(f"Generated frame {i + 1}/{frame_count}: {filename}")

    print(f"Generated {frame_count} test frames in '{output_dir}'.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate synthetic colored test frames for afterimage processing.")
    parser.add_argument("--output_dir", default=None, help="Output directory (default: ModelConfig.DEFAULT_INPUT_DIR)")
    parser.add_argument("--frame_count", type=int, default=30, help="Number of frames to generate")
    parser.add_argument("--height", type=int, default=500, help="Frame height")
    parser.add_argument("--width", type=int, default=500, help="Frame width")
    args = parser.parse_args()

    generate_test_frames(
        output_dir=args.output_dir,
        frame_count=args.frame_count,
        image_size=(args.height, args.width)
    )
