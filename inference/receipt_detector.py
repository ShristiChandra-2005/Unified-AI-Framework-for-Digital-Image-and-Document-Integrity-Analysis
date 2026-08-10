from pathlib import Path
from time import perf_counter
from typing import Any

from inference.field_extractor import extract_receipt_fields
from inference.integrity_scorer import calculate_integrity_score
from inference.metadata_validator import validate_receipt_fields
from inference.ocr_engine import OCREngine
from utils.file_utils import create_report_id, validate_image_path
from utils.helper import clean_metric, generate_receipt_summary
from utils.logger import get_logger, log_prediction
from utils.report_builder import (
    build_error_report,
    build_processing_info,
    build_receipt_report,
    save_report,
)

logger = get_logger(__name__)

MODULE_NAME = "Module 2 - Receipt Verification"


class ReceiptVerifier:
    """
    Module 2 receipt verification backend.

    This module does NOT use a trained deep learning model.

    Pipeline:
    Receipt image
        -> image preprocessing
        -> EasyOCR text extraction
        -> receipt field extraction
        -> metadata validation
        -> integrity scoring
        -> JSON report
        -> PDF report

    Important:
    - No model metadata.
    - No Grad-CAM.
    - No heatmap.
    - No probabilities.
    """

    def __init__(self, use_gpu: bool = False) -> None:
        self.ocr_engine = OCREngine(gpu=use_gpu)

    def verify(self, image_path: str | Path) -> dict[str, Any]:
        try:
            start_time = perf_counter()
            path = validate_image_path(image_path)

            ocr_start = perf_counter()
            ocr_result = self.ocr_engine.read_receipt(path)
            ocr_time_ms = round((perf_counter() - ocr_start) * 1000, 2)

            detected_text = str(ocr_result.get("detected_text", ""))
            receipt_fields = extract_receipt_fields(detected_text)

            validation = validate_receipt_fields(receipt_fields)

            integrity = calculate_integrity_score(
                fields=receipt_fields,
                validation=validation,
                ocr_confidence=float(ocr_result.get("ocr_confidence", 0.0)),
            )

            processing_time_ms = round((perf_counter() - start_time) * 1000, 2)

            processing = build_processing_info(
                time_ms=processing_time_ms,
                image_path=path,
            )
            processing["ocr_time_ms"] = ocr_time_ms

            decision_summary = generate_receipt_summary(
                receipt=receipt_fields,
                validation=validation,
                integrity=integrity,
            )

            report_id = create_report_id("module2")

            report = build_receipt_report(
                image_path=path,
                ocr=ocr_result,
                receipt=receipt_fields,
                validation=validation,
                integrity=integrity,
                decision_summary=decision_summary,
                processing=processing,
                report_id=report_id,
            )

            # build_receipt_report() already sets prediction / receipt_status /
            # confidence / risk_level / risk_score / status / validation_status /
            # merchant / invoice_number / invoice_date / total_amount /
            # integrity_score through clean_metric(). Do NOT re-set them here
            # with raw values - that reintroduces the mixed float/"N/A" types
            # that crashed the Streamlit table. Only the fields it doesn't
            # already cover are added below, and always through clean_metric().
            report["module"] = MODULE_NAME
            report["subtotal"] = clean_metric(receipt_fields.get("subtotal"))
            report["tax"] = clean_metric(receipt_fields.get("tax"))
            report["currency"] = clean_metric(receipt_fields.get("currency"))
            report["phone"] = clean_metric(receipt_fields.get("phone"))
            report["address"] = clean_metric(receipt_fields.get("address"))
            report["ocr_time_ms"] = clean_metric(ocr_time_ms)

            # Module 2 must not expose model/Grad-CAM/probability fields.
            report.pop("model", None)
            report.pop("dataset", None)
            report.pop("metrics", None)
            report.pop("probabilities", None)
            report.pop("visualization", None)
            report.pop("visualization_path", None)
            report.pop("visualization_error", None)
            report.pop("gradcam_path", None)
            report.pop("heatmap_path", None)

            save_report(report)
            log_prediction(logger, report)

            return report

        except Exception as error:
            logger.exception("Module 2 receipt verification failed")

            return build_error_report(
                module=MODULE_NAME,
                image_path=image_path,
                error=error,
            )


def verify_receipt(image_path: str | Path) -> dict[str, Any]:
    verifier = ReceiptVerifier(use_gpu=False)
    return verifier.verify(image_path)