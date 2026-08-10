from pathlib import Path
from typing import Any

import easyocr
import numpy as np

from preprocessing.receipt_preprocessing import preprocess_receipt_image


class OCREngine:
    """
    EasyOCR wrapper for receipt OCR.
    """

    def __init__(self, languages: list[str] | None = None, gpu: bool = False) -> None:
        self.languages = languages or ["en"]
        self.reader = easyocr.Reader(self.languages, gpu=gpu)

    def read_receipt(self, image_path: str | Path) -> dict[str, Any]:
        image = preprocess_receipt_image(image_path)

        results = self.reader.readtext(
            image,
            detail=1,
            paragraph=False,
            contrast_ths=0.05,
            adjust_contrast=0.7,
            text_threshold=0.6,
            low_text=0.3,
            link_threshold=0.4,
            mag_ratio=1.5,
        )

        lines: list[str] = []
        confidences: list[float] = []
        boxes: list[list[list[float]]] = []

        for box, text, confidence in results:
            clean_text = str(text).strip()

            if not clean_text:
                continue

            lines.append(clean_text)
            confidences.append(float(confidence))
            boxes.append([[float(point[0]), float(point[1])] for point in box])

        ocr_confidence = float(np.mean(confidences) * 100) if confidences else 0.0

        return {
            "detected_text": "\n".join(lines),
            "detected_words": lines,
            "boxes": boxes,
            "word_confidences": confidences,
            "ocr_confidence": round(ocr_confidence, 2),
            "line_count": len(lines),
        }
