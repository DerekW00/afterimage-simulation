import cv2
import numpy as np
import os

def generate_test_frames(output_folder: str, frame_count: int = 30, image_size=(256, 256)):
    """
    Generate a test image sequence for afterimage processing.

    Parameters
    ----------
    output_folder : str
        Directory to save the generated frames.
    frame_count : int
        Number of frames to generate.
    image_size : tuple
        Dimensions of the generated images.
    """
    os.makedirs(output_folder, exist_ok=True)

    for i in range(frame_count):
        # Create a blank black image
        frame = np.zeros((image_size[0], image_size[1], 3), dtype=np.uint8)

        # Draw a moving white circle to simulate motion-based afterimages
        center_x = int(image_size[1] / 2 + 100 * np.sin(2 * np.pi * i / frame_count))
        center_y = int(image_size[0] / 2)
        radius = 30

        # Color changes to test chromatic afterimages (R→G→B pattern)
        color = (
            int(255 * (i % 3 == 0)),  # Red channel
            int(255 * (i % 3 == 1)),  # Green channel
            int(255 * (i % 3 == 2))   # Blue channel
        )

        # Draw the circle
        cv2.circle(frame, (center_x, center_y), radius, color, -1)

        # Add varying brightness
        brightness = int(100 + 155 * np.sin(2 * np.pi * i / frame_count))
        frame = cv2.add(frame, (brightness, brightness, brightness, 0))

        # Save the frame
        frame_name = f"frame_{i:04d}.jpg"
        frame_path = os.path.join(output_folder, frame_name)
        cv2.imwrite(frame_path, frame)

        print(f"Generated frame {i+1}/{frame_count}: {frame_path}")

    print(f"Generated {frame_count} test frames in '{output_folder}'.")


if __name__ == "__main__":
    generate_test_frames("data/afterimage/1_batch_prototype/input", frame_count=30)