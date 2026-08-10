from pathlib import Path
from typing import Any

from preprocessing.image_preprocessing import preprocess_for_model


def preprocess_for_tampering_model(image_path: str | Path) -> tuple[Any, Any]:
    """
    Preprocess image for Module 3 tampering detection.

    This wrapper keeps Module 3 separate from Module 1 even if both use
    the same model input preprocessing internally.
    """
    return preprocess_for_model(image_path)
