import matplotlib.pyplot as plt
import numpy as np


def display_image(image: np.ndarray, title: str = "Image", cmap: str = 'gray'):
    """
    Display an image using matplotlib.

    Parameters
    ----------
    image : np.ndarray
        Image array.
    title : str, optional
        Plot title (default: "Image").
    cmap : str, optional
        Color map to use (default: 'gray').
    """
    plt.figure(figsize=(6, 6))
    plt.imshow(image, cmap=cmap)
    plt.title(title)
    plt.axis('off')
    plt.show()


def save_visualization(image: np.ndarray, filename: str, cmap: str = 'gray'):
    """
    Save the visualization of an image to a file.

    Parameters
    ----------
    image : np.ndarray
        Image array.
    filename : str
        Filename to save the image.
    cmap : str, optional
        Color map to use (default: 'gray').
    """
    plt.figure(figsize=(6, 6))
    plt.imshow(image, cmap=cmap)
    plt.axis('off')
    plt.savefig(filename, bbox_inches='tight', pad_inches=0)
    plt.close()
