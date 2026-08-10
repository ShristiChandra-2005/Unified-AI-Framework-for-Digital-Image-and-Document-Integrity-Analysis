from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from config.settings import DEVICE, REPORTS_DIR
from utils.file_utils import save_json, timestamp
from utils.helper import clean_metric


PROJECT_NAME = "VeriShield AI"
PROJECT_SUBTITLE = "Enterprise Digital Fraud Detection & Integrity Platform"
BACKEND_VERSION = "1.0"
REPORT_VERSION = "v1"


def build_model_info(
    name: Any,
    version: Any = "N/A",
    dataset: Any = "N/A",
    accuracy: Any = "N/A",
    precision: Any = "N/A",
    recall: Any = "N/A",
    f1_score: Any = "N/A",
) -> dict[str, Any]:
    """
    Compatibility helper for Module 1 and Module 3 detectors.

    Module 2 does not use this because receipt verification is OCR +
    rule-based validation, not a trained PyTorch model.
    """
    return {
        "name": clean_metric(name),
        "version": clean_metric(version),
        "dataset": clean_metric(dataset),
        "accuracy": clean_metric(accuracy),
        "precision": clean_metric(precision),
        "recall": clean_metric(recall),
        "f1_score": clean_metric(f1_score),
    }


def build_processing_info(time_ms: float, image_path: str | Path) -> dict[str, Any]:
    return {
        "time_ms": clean_metric(time_ms),
        "device": str(DEVICE),
        "timestamp": timestamp(),
        "image_path": str(image_path),
    }


def build_visualization_info(
    gradcam_path: str | None = None,
    heatmap_path: str | None = None,
    overlay_path: str | None = None,
    error: str | None = None,
) -> dict[str, Any]:
    return {
        "gradcam": gradcam_path,
        "heatmap": heatmap_path,
        "overlay": overlay_path or gradcam_path,
        "error": clean_metric(error),
    }


def build_prediction_report(
    module: str,
    image_path: str | Path,
    prediction: str,
    confidence: float,
    confidence_label_value: str,
    risk_level: str,
    risk_score: float,
    decision_summary: dict[str, Any],
    model: dict[str, Any],
    processing: dict[str, Any],
    visualization: dict[str, Any],
    probabilities: dict[str, float],
    report_id: str,
    model_load_mode: str | None = None,
) -> dict[str, Any]:
    """
    Build report for Module 1 and Module 3.

    Training metrics are intentionally kept inside the model object only for
    internal traceability. UI/PDF should focus on inference result.
    """
    visual_path = visualization.get("overlay") or visualization.get("gradcam")
    cleaned_model = _clean_dict(model)

    report = {
        "success": True,
        "project_name": PROJECT_NAME,
        "project_subtitle": PROJECT_SUBTITLE,
        "backend_version": BACKEND_VERSION,
        "report_version": REPORT_VERSION,
        "module": module,
        "prediction": clean_metric(prediction),
        "confidence": clean_metric(confidence),
        "confidence_label": clean_metric(confidence_label_value),
        "risk_level": clean_metric(risk_level),
        "risk_score": clean_metric(risk_score),
        "status": "Completed",
        "processing_time": clean_metric(processing.get("time_ms")),
        "processing_time_ms": clean_metric(processing.get("time_ms")),
        "timestamp": clean_metric(processing.get("timestamp")),
        "device": clean_metric(processing.get("device")),
        "report_id": clean_metric(report_id),
        "report_path": None,
        "pdf_report_path": None,
        "decision_summary": decision_summary,
        "visualization": visualization,
        "visualization_path": visual_path,
        "visualization_error": clean_metric(visualization.get("error")),
        "probabilities": probabilities,
        "uploaded_image": str(image_path),
        "image_path": str(image_path),
        "model": cleaned_model,
        "model_load_mode": clean_metric(model_load_mode),
        "details": {},
    }

    if module == "Module 1 - AI Generated Image Detection":
        report["gradcam_path"] = visual_path

    if module == "Module 3 - Image Tampering Detection":
        report["heatmap_path"] = visual_path

    return report


def build_receipt_report(
    image_path: str | Path,
    ocr: dict[str, Any],
    receipt: dict[str, Any],
    validation: dict[str, Any],
    integrity: dict[str, Any],
    decision_summary: dict[str, Any],
    processing: dict[str, Any],
    report_id: str,
) -> dict[str, Any]:
    """
    Build report for Module 2.

    Module 2 does not use a trained ML model. It uses:
    OCR -> field extraction -> validation -> integrity scoring.
    Therefore this report intentionally does not include model, dataset,
    metrics, Grad-CAM, or heatmap fields.
    """
    validation_status = validation.get("validation_status") or validation.get("status")
    receipt_status = integrity.get("status")
    integrity_score = integrity.get("integrity_score")

    return {
        "success": True,
        "project_name": PROJECT_NAME,
        "project_subtitle": PROJECT_SUBTITLE,
        "backend_version": BACKEND_VERSION,
        "report_version": REPORT_VERSION,
        "module": "Module 2 - Receipt Verification",
        "prediction": clean_metric(receipt_status),
        "receipt_status": clean_metric(receipt_status),
        "confidence": clean_metric(integrity_score),
        "confidence_label": _score_label(integrity_score),
        "risk_level": clean_metric(integrity.get("risk_level")),
        "risk_score": clean_metric(integrity.get("risk_score")),
        "status": clean_metric(validation.get("status")),
        "validation_status": clean_metric(validation_status),
        "processing_time": clean_metric(processing.get("time_ms")),
        "processing_time_ms": clean_metric(processing.get("time_ms")),
        "timestamp": clean_metric(processing.get("timestamp")),
        "device": clean_metric(processing.get("device")),
        "report_id": clean_metric(report_id),
        "report_path": None,
        "pdf_report_path": None,
        "decision_summary": decision_summary,
        "processing": processing,
        "ocr": ocr,
        "receipt": receipt,
        "fields": receipt,
        "validation": validation,
        "integrity": integrity,
        "uploaded_image": str(image_path),
        "image_path": str(image_path),
        "merchant": clean_metric(receipt.get("merchant")),
        "invoice_number": clean_metric(receipt.get("invoice_number")),
        "invoice_date": clean_metric(receipt.get("date")),
        "total_amount": clean_metric(receipt.get("total")),
        "integrity_score": clean_metric(integrity_score),
        "validation_checks": _build_validation_checks(validation),
        "details": {
            "ocr": ocr,
            "receipt": receipt,
            "validation": validation,
            "integrity": integrity,
        },
    }


def save_report(report: dict[str, Any]) -> Path:
    report_id = str(report["report_id"])

    json_path = REPORTS_DIR / f"{report_id}.json"
    pdf_path = REPORTS_DIR / f"{report_id}.pdf"

    report["report_path"] = str(json_path)

    try:
        generated_pdf = generate_pdf_report(report, pdf_path)
        report["pdf_report_path"] = str(generated_pdf)
        report["pdf_error"] = None
    except Exception as error:
        report["pdf_report_path"] = None
        report["pdf_error"] = str(error)

    report["report"] = {
        "id": report_id,
        "json": str(json_path),
        "pdf": report.get("pdf_report_path"),
        "created": report.get("timestamp"),
        "downloadable": True,
    }

    save_json(report, json_path)

    return json_path


def build_error_report(
    module: str,
    image_path: str | Path,
    error: Exception,
) -> dict[str, Any]:
    return {
        "success": False,
        "project_name": PROJECT_NAME,
        "project_subtitle": PROJECT_SUBTITLE,
        "backend_version": BACKEND_VERSION,
        "report_version": REPORT_VERSION,
        "module": module,
        "prediction": "N/A",
        "confidence": "N/A",
        "confidence_label": "N/A",
        "risk_level": "N/A",
        "risk_score": "N/A",
        "status": "Failed",
        "processing_time": "N/A",
        "processing_time_ms": "N/A",
        "timestamp": timestamp(),
        "device": str(DEVICE),
        "report_id": "N/A",
        "report_path": None,
        "pdf_report_path": None,
        "decision_summary": {
            "title": "Backend Error",
            "summary": [str(error)],
        },
        "visualization": build_visualization_info(error=str(error)),
        "visualization_path": None,
        "visualization_error": str(error),
        "probabilities": {},
        "validation": {},
        "integrity": {},
        "error": str(error),
        "image_path": str(image_path),
        "details": {},
    }


def generate_pdf_report(report: dict[str, Any], output_path: str | Path) -> Path:
    module = report.get("module", "")

    if module == "Module 2 - Receipt Verification":
        return generate_receipt_pdf(report, output_path)

    if module == "Module 3 - Image Tampering Detection":
        return generate_tampering_pdf(report, output_path)

    return generate_ai_pdf(report, output_path)


def generate_ai_pdf(report: dict[str, Any], output_path: str | Path) -> Path:
    styles, doc, story = _create_pdf(output_path)

    _add_title(story, styles, "AI Generated Image Detection Report")
    _add_report_metadata(story, report)

    story.append(Paragraph("Analysis Summary", styles["Heading2"]))

    data = [
        ["Prediction", clean_metric(report.get("prediction"))],
        ["Confidence", f"{clean_metric(report.get('confidence'))}%"],
        ["Confidence Label", clean_metric(report.get("confidence_label"))],
        ["Risk Score", clean_metric(report.get("risk_score"))],
        ["Risk Level", clean_metric(report.get("risk_level"))],
    ]

    story.append(_table(data))
    story.append(Spacer(1, 16))

    _add_decision_summary(story, styles, report)

    story.append(Paragraph("Grad-CAM Explainability", styles["Heading2"]))
    _add_optional_image(
        story=story,
        styles=styles,
        image_path=report.get("visualization_path") or report.get("gradcam_path"),
        fallback_text="Grad-CAM visualization not available.",
    )

    _add_footer(story, styles)
    doc.build(story)

    return Path(output_path)


def generate_receipt_pdf(report: dict[str, Any], output_path: str | Path) -> Path:
    styles, doc, story = _create_pdf(output_path)

    _add_title(story, styles, "Receipt Verification Report")
    _add_report_metadata(story, report)

    receipt = report.get("receipt", {})
    validation = report.get("validation", {})
    integrity = report.get("integrity", {})

    story.append(Paragraph("Receipt Analysis", styles["Heading2"]))

    receipt_data = [
        ["Receipt Status", clean_metric(report.get("receipt_status"))],
        ["Merchant", clean_metric(receipt.get("merchant"))],
        ["Invoice Number", clean_metric(receipt.get("invoice_number"))],
        ["Invoice Date", clean_metric(receipt.get("date"))],
        ["Subtotal", clean_metric(receipt.get("subtotal"))],
        ["Tax", clean_metric(receipt.get("tax"))],
        ["Total Amount", clean_metric(receipt.get("total"))],
        ["Currency", clean_metric(receipt.get("currency"))],
        ["Phone", clean_metric(receipt.get("phone"))],
        ["Address", clean_metric(receipt.get("address"))],
        ["Integrity Score", clean_metric(integrity.get("integrity_score"))],
        ["Risk Level", clean_metric(integrity.get("risk_level"))],
    ]

    story.append(_table(receipt_data))
    story.append(Spacer(1, 16))

    story.append(Paragraph("Validation Checklist", styles["Heading2"]))

    validation_rows = [["Check", "Result"]]

    for item in _build_validation_checks(validation):
        validation_rows.append([item["check"], item["result"]])

    story.append(_table(validation_rows))
    story.append(Spacer(1, 16))

    _add_decision_summary(story, styles, report)

    _add_footer(story, styles)
    doc.build(story)

    return Path(output_path)


def generate_tampering_pdf(report: dict[str, Any], output_path: str | Path) -> Path:
    styles, doc, story = _create_pdf(output_path)

    _add_title(story, styles, "Image Tampering Analysis Report")
    _add_report_metadata(story, report)

    details = report.get("details", {})

    story.append(Paragraph("Tampering Analysis", styles["Heading2"]))

    tampering_data = [
        ["Prediction", clean_metric(report.get("prediction"))],
        ["Confidence", f"{clean_metric(report.get('confidence'))}%"],
        ["Risk Level", clean_metric(report.get("risk_level"))],
        ["Risk Score", clean_metric(report.get("risk_score"))],
        [
            "Tampering Type",
            clean_metric(details.get("tampering_type") or report.get("tampering_type")),
        ],
        [
            "Affected Region",
            clean_metric(details.get("affected_region") or report.get("affected_region")),
        ],
        [
            "Localization Status",
            clean_metric(
                details.get("localization_status") or report.get("localization_status")
            ),
        ],
        [
            "Recommendation",
            clean_metric(details.get("recommendation") or report.get("recommendation")),
        ],
    ]

    story.append(_table(tampering_data))
    story.append(Spacer(1, 16))

    _add_decision_summary(story, styles, report)

    story.append(Paragraph("Tampering Heatmap", styles["Heading2"]))
    _add_optional_image(
        story=story,
        styles=styles,
        image_path=report.get("visualization_path") or report.get("heatmap_path"),
        fallback_text="Tampering heatmap not available.",
    )

    _add_footer(story, styles)
    doc.build(story)

    return Path(output_path)


def _create_pdf(output_path: str | Path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(str(output_path), pagesize=A4)
    story = []

    return styles, doc, story


def _add_title(story: list[Any], styles: Any, report_title: str) -> None:
    story.append(Paragraph(PROJECT_NAME, styles["Title"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(PROJECT_SUBTITLE, styles["BodyText"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(report_title, styles["Heading1"]))
    story.append(Spacer(1, 12))


def _add_report_metadata(story: list[Any], report: dict[str, Any]) -> None:
    data = [
        ["Report ID", clean_metric(report.get("report_id"))],
        ["Timestamp", clean_metric(report.get("timestamp"))],
        ["Version", REPORT_VERSION],
        ["Processing Time", f"{clean_metric(report.get('processing_time_ms'))} ms"],
        ["Device", clean_metric(report.get("device"))],
    ]

    story.append(_table(data))
    story.append(Spacer(1, 16))


def _add_decision_summary(
    story: list[Any],
    styles: Any,
    report: dict[str, Any],
) -> None:
    summary = report.get("decision_summary", {})
    points = summary.get("summary", [])

    story.append(Paragraph("Decision Summary", styles["Heading2"]))

    if not points:
        story.append(Paragraph("No decision summary available.", styles["BodyText"]))
        story.append(Spacer(1, 16))
        return

    labels = ["Overview", "Analysis", "Recommendation"]

    for index, point in enumerate(points[:3]):
        label = labels[index] if index < len(labels) else "Note"
        story.append(Paragraph(f"<b>{label}</b>", styles["BodyText"]))
        story.append(Paragraph(str(point), styles["BodyText"]))
        story.append(Spacer(1, 6))

    for point in points[3:]:
        story.append(Paragraph(str(point), styles["BodyText"]))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 12))


def _add_optional_image(
    story: list[Any],
    styles: Any,
    image_path: str | None,
    fallback_text: str,
) -> None:
    if image_path and Path(image_path).exists():
        try:
            story.append(Image(str(image_path), width=300, height=220))
            story.append(Spacer(1, 16))
            return
        except Exception:
            pass

    story.append(Paragraph(fallback_text, styles["BodyText"]))
    story.append(Spacer(1, 16))


def _add_footer(story: list[Any], styles: Any) -> None:
    story.append(Spacer(1, 20))
    story.append(Paragraph("Developed by Shristi Chandra", styles["Italic"]))


def _table(data: list[list[Any]]) -> Table:
    table = Table(data, colWidths=[150, 330])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E5E7EB")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )

    return table


def _score_label(score: Any) -> str:
    try:
        score = float(score)
    except (TypeError, ValueError):
        return "N/A"

    if score >= 95:
        return "Very High"

    if score >= 85:
        return "High"

    if score >= 70:
        return "Medium"

    if score >= 50:
        return "Low"

    return "Very Low"


def _clean_dict(data: dict[str, Any]) -> dict[str, Any]:
    return {key: clean_metric(value) for key, value in data.items()}


def _build_validation_checks(validation: dict[str, Any]) -> list[dict[str, str]]:
    checks = {
        "Merchant Found": validation.get("merchant_found"),
        "Invoice Found": validation.get("invoice_found"),
        "Date Found": validation.get("date_found"),
        "Date Valid": validation.get("date_valid"),
        "Amount Valid": validation.get("amount_valid"),
        "Tax Consistent": validation.get("tax_consistent"),
    }

    return [
        {
            "check": name,
            "result": "Passed" if value else "Review Needed",
        }
        for name, value in checks.items()
    ]
