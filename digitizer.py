import numpy as np
from PIL import Image


def load_image(image_path):
    """Load an image and convert to grayscale numpy array."""
    img = Image.open(image_path).convert("L")  # L = grayscale
    return np.array(img)


def extract_curve(image_array, x_min=10, x_max=80):
    """
    Scan each column of the image and find the darkest pixel row.
    That row represents the XRD curve at that 2-theta position.

    Returns:
        two_theta: array of 2-theta values
        intensity: array of normalized intensity values (0 to 1)
    """
    height, width = image_array.shape

    pixel_rows = []

    for col in range(width):
        column = image_array[:, col]
        darkest_row = np.argmin(column)  # darkest pixel = the curve line
        pixel_rows.append(darkest_row)

    pixel_rows = np.array(pixel_rows)

    # Convert pixel positions to real axis values
    two_theta = np.linspace(x_min, x_max, width)

    # Flip intensity: top of image = high intensity, bottom = low
    intensity = 1.0 - (pixel_rows / height)

    return two_theta, intensity


def digitize_image(image_path, x_min=10, x_max=80):
    """
    Full pipeline: load image → extract curve → return values.
    """
    image_array = load_image(image_path)
    two_theta, intensity = extract_curve(image_array, x_min, x_max)
    return two_theta, intensity


# Quick test when you run this file directly
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # Replace this path with any XRD image you have
    test_path = "test_xrd.png"

    try:
        two_theta, intensity = digitize_image(test_path, x_min=10, x_max=80)
        plt.plot(two_theta, intensity)
        plt.xlabel("2θ (degrees)")
        plt.ylabel("Intensity")
        plt.title("Extracted XRD Curve")
        plt.show()
    except FileNotFoundError:
        print("No test image found — digitizer.py is ready to use.")
