import sys

try:
    import numpy as np
    import cv2
    import matplotlib.pyplot as plt
except ModuleNotFoundError as e:
    print(f"Error: {e}. Please ensure all dependencies are installed.")
    sys.exit(1)


def load_image(image_path):
    """Loads an image and converts it to RGB."""
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found at path: {image_path}")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


def apply_afterimage_effect(image, decay_factor=0.8):
    """Applies a simple afterimage effect using opponent color processing and decay."""

    # Ensure image is a NumPy array
    if not isinstance(image, np.ndarray):
        raise TypeError("Input image must be a NumPy array")

    # Convert to float for processing
    img_float = image.astype(np.float32) / 255.0

    # Opponent color processing (inverting colors as a basic afterimage effect)
    afterimage = 1.0 - img_float  # Simple inversion for demonstration

    # Apply decay factor (simulating gradual fading)
    afterimage *= decay_factor

    # Clip values to stay within valid range
    afterimage = np.clip(afterimage, 0, 1)

    # Convert back to uint8
    afterimage = (afterimage * 255).astype(np.uint8)

    return afterimage


def display_images(original, afterimage):
    """Displays the original and afterimage side by side."""
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    ax[0].imshow(original)
    ax[0].set_title("Original Image")
    ax[0].axis("off")

    ax[1].imshow(afterimage)
    ax[1].set_title("Afterimage Effect")
    ax[1].axis("off")

    plt.show()


if __name__ == "__main__":
    try:
        # Load a sample image
        image_path = "data/sample.jpg"  # Replace with an actual image path
        img = load_image(image_path)

        # Apply afterimage effect
        afterimage = apply_afterimage_effect(img)

        # Display the results
        display_images(img, afterimage)
    except Exception as e:
        print(f"An error occurred : {e}")
        sys.exit(1)
