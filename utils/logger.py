import logging
from typing import Any

from config.settings import REPORTS_DIR


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    log_path = REPORTS_DIR / "phase3_backend.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def log_prediction(logger: logging.Logger, result: dict[str, Any]) -> None:
    module = result.get("module", "Unknown Module")
    prediction = result.get("prediction", "N/A")
    confidence = result.get("confidence", "N/A")
    risk_level = result.get("risk_level", "N/A")
    status = result.get("status", "N/A")

    processing_time = (
        result.get("processing_time_ms")
        or result.get("processing_time")
        or result.get("processing", {}).get("time_ms")
        or "N/A"
    )

    report_id = result.get("report_id") or result.get("report", {}).get("id") or "N/A"
    report_path = result.get("report_path") or result.get("report", {}).get("json") or "N/A"
    pdf_path = result.get("pdf_report_path") or result.get("report", {}).get("pdf") or "N/A"

    if module == "Module 2 - Receipt Verification":
        logger.info(
            "Module=%s | Engine=EasyOCR | Validation=Metadata Rules | "
            "ReceiptStatus=%s | IntegrityScore=%s | Risk=%s | Status=%s | "
            "Time=%s ms | ReportID=%s | JSON=%s | PDF=%s",
            module,
            prediction,
            confidence,
            risk_level,
            status,
            processing_time,
            report_id,
            report_path,
            pdf_path,
        )
        return

    model = result.get("model", {})
    model_name = model.get("name", "N/A")
    dataset = model.get("dataset", "N/A")

    visualization_path = (
        result.get("visualization_path")
        or result.get("gradcam_path")
        or result.get("heatmap_path")
        or result.get("visualization", {}).get("overlay")
        or "N/A"
    )

    logger.info(
        "Module=%s | Model=%s | Dataset=%s | Prediction=%s | Confidence=%s | "
        "Risk=%s | Time=%s ms | Visualization=%s | ReportID=%s | JSON=%s | PDF=%s",
        module,
        model_name,
        dataset,
        prediction,
        confidence,
        risk_level,
        processing_time,
        visualization_path,
        report_id,
        report_path,
        pdf_path,
    )


def log_error(logger: logging.Logger, module: str, error: Exception) -> None:
    logger.exception("%s failed: %s", module, error)
