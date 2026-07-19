import numpy as np
from PIL import Image


def load_image(image_path):
    img = Image.open(image_path).convert("L")
    return np.array(img)


def extract_curve(image_array, x_min=10, x_max=80):
    height, width = image_array.shape
    pixel_rows = []

    for col in range(width):
        column = image_array[:, col]
        darkest_row = np.argmin(column)
        pixel_rows.append(darkest_row)

    pixel_rows = np.array(pixel_rows)
    two_theta = np.linspace(x_min, x_max, width)
    intensity = 1.0 - (pixel_rows / height)

    return two_theta, intensity


def digitize_image(image_path, x_min=10, x_max=80):
    image_array = load_image(image_path)
    two_theta, intensity = extract_curve(image_array, x_min, x_max)
    return two_theta, intensity


if __name__ == "__main__":
    import matplotlib.pyplot as plt

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
