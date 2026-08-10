from typing import Any


def calculate_integrity_score(
    fields: dict[str, Any],
    validation: dict[str, Any],
    ocr_confidence: float,
) -> dict[str, Any]:
    """
    Calculate final receipt integrity score.

    Score composition:
    OCR confidence: 30%
    Metadata validation: 35%
    Field completeness: 20%
    Logical consistency: 15%
    """
    completeness_score = _field_completeness_score(fields)
    metadata_score = _metadata_validation_score(validation)
    logic_score = _logical_consistency_score(validation)

    final_score = (
        0.30 * float(ocr_confidence)
        + 0.35 * metadata_score
        + 0.20 * completeness_score
        + 0.15 * logic_score
    )

    final_score = round(float(final_score), 2)
    risk_score = round(100.0 - final_score, 2)

    if final_score >= 85:
        status = "Trusted"
        risk_level = "Low"
    elif final_score >= 60:
        status = "Suspicious"
        risk_level = "Medium"
    else:
        status = "Manipulated"
        risk_level = "High"

    return {
        "ocr_score": round(float(ocr_confidence), 2),
        "metadata_score": round(metadata_score, 2),
        "field_completeness_score": round(completeness_score, 2),
        "logical_consistency_score": round(logic_score, 2),
        "integrity_score": final_score,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "status": status,
    }


def _field_completeness_score(fields: dict[str, Any]) -> float:
    required_fields = [
        "merchant",
        "date",
        "invoice_number",
        "subtotal",
        "tax",
        "total",
        "currency",
        "phone",
        "address",
    ]

    present = sum(1 for field in required_fields if fields.get(field))

    return round((present / len(required_fields)) * 100, 2)


def _metadata_validation_score(validation: dict[str, Any]) -> float:
    status = validation.get("status")

    if status == "PASS":
        return 100.0

    if status == "WARNING":
        return 75.0

    return 35.0


def _logical_consistency_score(validation: dict[str, Any]) -> float:
    issues = len(validation.get("issues", []))
    warnings = len(validation.get("warnings", []))

    score = 100.0 - issues * 25.0 - warnings * 10.0

    if validation.get("tax_consistent") is False:
        score -= 15.0

    if validation.get("date_valid") is False and validation.get("date_found"):
        score -= 5.0

    return max(0.0, score)
