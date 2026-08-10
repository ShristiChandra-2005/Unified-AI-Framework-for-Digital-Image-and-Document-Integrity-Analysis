from pathlib import Path

import cv2
import numpy as np

from utils.file_utils import validate_image_path


def preprocess_receipt_image(image_path: str | Path) -> np.ndarray:
    """
    Preprocess receipt image for OCR.

    This function improves text readability without changing the receipt content.
    It is designed for EasyOCR and works well for SROIE/CORD style receipts.
    """
    path = validate_image_path(image_path)

    image = cv2.imread(str(path))

    if image is None:
        raise ValueError(f"Could not read receipt image: {path}")

    image = _resize_for_ocr(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    denoised = cv2.fastNlMeansDenoising(gray, None, h=12, templateWindowSize=7, searchWindowSize=21)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(denoised)

    sharpened = _sharpen_image(enhanced)

    return sharpened


def _resize_for_ocr(image: np.ndarray, min_width: int = 900) -> np.ndarray:
    height, width = image.shape[:2]

    if width >= min_width:
        return image

    scale = min_width / width
    new_size = (int(width * scale), int(height * scale))

    return cv2.resize(image, new_size, interpolation=cv2.INTER_CUBIC)


def _sharpen_image(image: np.ndarray) -> np.ndarray:
    kernel = np.array(
        [
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0],
        ]
    )

    return cv2.filter2D(image, -1, kernel)
