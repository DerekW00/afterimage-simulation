import numpy as np
from model.afterimage import generate_afterimage


def test_generate_afterimage():
    # Create a dummy gradient image (256x256)
    dummy_image = np.tile(np.linspace(0, 255, 256, dtype=np.uint8), (256, 1))
    params = {'intensity': 1.0, 'ca': 0.3, 'cd': 0.3, 'dt': 0.032, 'iterations': 10}
    result = generate_afterimage(dummy_image, params)

    # Assert the result has the same shape and type as the input
    assert result.shape == dummy_image.shape
    assert result.dtype == np.uint8


if __name__ == "__main__":
    test_generate_afterimage()
    print("afterimage test passed.")