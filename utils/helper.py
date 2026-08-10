from typing import Any


def clean_metric(value: Any) -> str:
    """
    Normalize any report value into one consistent, display-safe type.

    This used to return `value` unchanged when it wasn't None, so a real
    number (45.99) and a missing value ("N/A") ended up as different
    Python types in the same report field. When that report field is
    later put into a Streamlit table or PDF table, mixing float and str
    in one column is exactly what crashes Arrow with:
    "Expected bytes, got a 'float' object".

    Now every non-empty value is always turned into a string, so a
    column is never a mix of types again.
    """
    if value is None or value == "":
        return "N/A"

    if isinstance(value, bool):
        return "Yes" if value else "No"

    if isinstance(value, float):
        # Avoid floating point noise like 83.33000000000001
        return f"{value:.2f}"

    return str(value)


def confidence_label(confidence: float | int | None) -> str:
    if confidence is None:
        return "N/A"

    confidence = float(confidence)

    if confidence >= 95:
        return "Very High"
    if confidence >= 85:
        return "High"
    if confidence >= 70:
        return "Medium"
    if confidence >= 50:
        return "Low"

    return "Very Low"


def get_risk_level_and_score(prediction: str, confidence: float) -> tuple[str, float]:
    suspicious_words = [
        "fake",
        "ai",
        "generated",
        "tampered",
        "manipulated",
        "suspicious",
    ]

    prediction_lower = str(prediction).lower()
    is_suspicious = any(word in prediction_lower for word in suspicious_words)

    risk_score = confidence if is_suspicious else 100 - confidence
    risk_score = round(float(risk_score), 2)

    if risk_score >= 75:
        return "High", risk_score

    if risk_score >= 45:
        return "Medium", risk_score

    return "Low", risk_score


def generate_ai_summary(
    prediction: str,
    confidence: float,
    risk_level: str,
    gradcam_path: str | None = None,
    visualization_error: str | None = None,
) -> dict[str, Any]:
    summary = [
        f"The uploaded image has been classified as {prediction}.",
        f"The model confidence is {confidence:.2f}% ({confidence_label(confidence)}).",
    ]

    if risk_level == "High":
        summary.append("Synthetic visual artifacts or AI-generated patterns were strongly detected.")
    elif risk_level == "Medium":
        summary.append("The image shows moderate uncertainty and should be reviewed manually.")
    else:
        summary.append("The image appears less suspicious according to the current model output.")

    if gradcam_path:
        summary.append("Grad-CAM visualization supports the prediction by highlighting influential image regions.")
    elif visualization_error:
        summary.append(f"Grad-CAM was unavailable because: {visualization_error}")
    else:
        summary.append("Grad-CAM visualization was not generated.")

    summary.append(f"Overall risk level: {risk_level}.")

    return {
        "title": f"{risk_level} Risk AI Image Decision",
        "prediction": prediction,
        "confidence": f"{confidence:.2f}%",
        "risk": risk_level,
        "summary": summary,
    }


def generate_tampering_summary(
    prediction: str,
    confidence: float,
    risk_level: str,
    gradcam_path: str | None = None,
    visualization_error: str | None = None,
) -> dict[str, Any]:
    summary = [
        f"Manipulation status: {prediction}.",
        f"The tampering detector confidence is {confidence:.2f}% ({confidence_label(confidence)}).",
    ]

    if prediction == "Tampered":
        summary.append("The image contains visual patterns consistent with possible digital manipulation.")
    else:
        summary.append("The image appears authentic based on the current tampering detection model.")

    if risk_level == "High":
        summary.append("Risk level is high, so manual forensic verification is recommended.")
    elif risk_level == "Medium":
        summary.append("Risk level is medium, so the image should be reviewed before acceptance.")
    else:
        summary.append("Risk level is low according to the current model output.")

    if gradcam_path:
        summary.append("Tampering heatmap is available and highlights the region used for the model decision.")
    elif visualization_error:
        summary.append(f"Localization is unavailable because: {visualization_error}")
    else:
        summary.append("Localization unavailable.")

    recommendation = (
        "Manual verification recommended before using this image as trusted evidence."
        if prediction == "Tampered"
        else "Image can be treated as low-risk, subject to normal verification."
    )

    summary.append(f"Recommendation: {recommendation}")

    return {
        "title": f"{risk_level} Risk Image Tampering Decision",
        "prediction": prediction,
        "confidence": f"{confidence:.2f}%",
        "risk": risk_level,
        "recommendation": recommendation,
        "summary": summary,
    }


def generate_receipt_summary(
    receipt: dict[str, Any],
    validation: dict[str, Any],
    integrity: dict[str, Any],
) -> dict[str, Any]:
    validation_status = validation.get("validation_status") or validation.get("status", "Unknown")
    receipt_status = integrity.get("status", "N/A")
    integrity_score = integrity.get("integrity_score", "N/A")
    risk_level = integrity.get("risk_level", "N/A")

    summary = [
        f"Receipt status: {receipt_status}.",
        f"Merchant detected: {receipt.get('merchant') or 'Not detected'}.",
        f"Invoice number: {receipt.get('invoice_number') or 'Not detected'}.",
        f"Date detected: {receipt.get('date') or 'Not detected'}.",
        f"Total amount detected: {receipt.get('total') or 'Not detected'}.",
        f"Validation status: {validation_status}.",
        f"Integrity score: {integrity_score}.",
        f"Overall risk level: {risk_level}.",
    ]

    if validation_status == "PASS":
        summary.append("OCR and metadata validation checks passed successfully.")
    elif validation_status == "WARNING":
        summary.append("Receipt is usable, but one or more fields require manual review.")
    else:
        summary.append("Receipt verification failed because mandatory fields or logical checks did not pass.")

    if receipt_status == "Trusted":
        recommendation = "Receipt appears authentic."
    elif receipt_status == "Suspicious":
        recommendation = "Manual verification is recommended before accepting this receipt."
    else:
        recommendation = "Receipt appears highly suspicious and should not be trusted without investigation."

    summary.append(f"Recommendation: {recommendation}")

    return {
        "title": f"{risk_level} Risk Receipt Verification Decision",
        "receipt_status": receipt_status,
        "merchant": receipt.get("merchant"),
        "invoice_number": receipt.get("invoice_number"),
        "date": receipt.get("date"),
        "total": receipt.get("total"),
        "validation_status": validation_status,
        "integrity_score": integrity_score,
        "risk": risk_level,
        "recommendation": recommendation,
        "summary": summary,
    }