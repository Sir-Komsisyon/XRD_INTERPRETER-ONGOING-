import numpy as np
from PIL import Image
import fitz  # pymupdf
import docx
import io


def load_image(image_path):
    """Load PNG/JPG directly."""
    img = Image.open(image_path).convert("L")
    return np.array(img)


def pdf_to_image(pdf_path):
    """Extract first page of PDF as grayscale numpy array."""
    doc = fitz.open(pdf_path)
    page = doc[0]
    mat = fitz.Matrix(2, 2)
    pix = page.get_pixmap(matrix=mat, colorspace=fitz.csGRAY)
    img_array = np.frombuffer(pix.samples, dtype=np.uint8)
    img_array = img_array.reshape(pix.height, pix.width)
    return img_array


def docx_to_image(docx_path):
    """Extract first image found in a Word document."""
    document = docx.Document(docx_path)
    for rel in document.part.rels.values():
        if "image" in rel.reltype:
            image_data = rel.target_part.blob
            img = Image.open(io.BytesIO(image_data)).convert("L")
            return np.array(img)
    raise ValueError("No image found in the Word document.")


def extract_curve(image_array, x_min=10, x_max=80):
    """Scan each column and find the curve line."""
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


def digitize_image(file_path, x_min=10, x_max=80):
    """
    Auto-detect file type and extract XRD curve.
    Supports: PNG, JPG, PDF, DOCX
    """
    ext = file_path.lower()

    if ext.endswith(".pdf"):
        image_array = pdf_to_image(file_path)

    elif ext.endswith(".docx"):
        image_array = docx_to_image(file_path)

    elif ext.endswith(".png") or ext.endswith(".jpg") or ext.endswith(".jpeg"):
        image_array = load_image(file_path)

    else:
        raise ValueError(f"Unsupported file type: {file_path}")

    two_theta, intensity = extract_curve(image_array, x_min, x_max)
    return two_theta, intensity


if __name__ == "__main__":
    print("digitizer.py loaded successfully.")
