from datetime import datetime
from typing import Any


MANDATORY_FIELDS = ["merchant", "date", "total"]


def _is_missing(value: Any) -> bool:
    """A field is missing only if it's None or an empty/whitespace string.

    `if not fields.get(field)` treats a real 0 (e.g. a $0 tax amount) as
    "missing" too, since 0 is falsy in Python. That silently mislabels a
    correct value as an error. This checks explicitly for None/empty
    instead, so a real 0 stays valid.
    """
    if value is None:
        return True
    return str(value).strip() == ""


def validate_receipt_fields(fields: dict[str, Any]) -> dict[str, Any]:
    """
    Validate extracted receipt fields using rule-based checks.
    """
    issues: list[str] = []
    warnings: list[str] = []

    missing_fields = [
        field for field in MANDATORY_FIELDS
        if _is_missing(fields.get(field))
    ]

    for field in missing_fields:
        issues.append(f"Missing mandatory field: {field}")

    date_valid = _validate_date(fields.get("date"))

    if fields.get("date") and not date_valid:
        warnings.append("Date format could not be confidently validated")

    subtotal = _to_float(fields.get("subtotal"))
    tax = _to_float(fields.get("tax"))
    total = _to_float(fields.get("total"))

    amount_valid = total is not None and total > 0

    if not _is_missing(fields.get("total")) and not amount_valid:
        issues.append("Invalid total amount")

    tax_consistent = True

    if subtotal is not None and tax is not None and total is not None:
        expected_total = subtotal + tax
        tolerance = max(1.0, total * 0.05)

        if abs(expected_total - total) > tolerance:
            tax_consistent = False
            warnings.append("Subtotal + tax does not match total")

    duplicate_fields = _find_duplicate_amounts(fields)

    if duplicate_fields:
        warnings.append(f"Duplicate amount values detected: {', '.join(duplicate_fields)}")

    if _is_missing(fields.get("invoice_number")):
        warnings.append("Invoice number not detected")

    if _is_missing(fields.get("currency")):
        warnings.append("Currency not detected")

    if issues:
        status = "FAIL"
    elif warnings:
        status = "WARNING"
    else:
        status = "PASS"

    return {
        "status": status,
        "validation_status": status,
        "merchant_found": not _is_missing(fields.get("merchant")),
        "invoice_found": not _is_missing(fields.get("invoice_number")),
        "date_found": not _is_missing(fields.get("date")),
        "date_valid": date_valid,
        "total_found": not _is_missing(fields.get("total")),
        "amount_valid": amount_valid,
        "tax_consistent": tax_consistent,
        "duplicate_fields": duplicate_fields,
        "missing_fields": missing_fields,
        "warnings": warnings,
        "issues": issues,
    }


def _validate_date(value: Any) -> bool:
    if not value:
        return False

    value = str(value).strip()

    formats = [
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%d-%m-%y",
        "%d/%m/%y",
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d %b %Y",
        "%d %B %Y",
        "%b %d %Y",
        "%B %d %Y",
        "%b %d, %Y",
        "%B %d, %Y",
    ]

    for date_format in formats:
        try:
            datetime.strptime(value, date_format)
            return True
        except ValueError:
            continue

    return False


def _find_duplicate_amounts(fields: dict[str, Any]) -> list[str]:
    amount_fields = ["subtotal", "tax", "total"]
    values: dict[float, list[str]] = {}

    for field in amount_fields:
        amount = _to_float(fields.get(field))

        if amount is None:
            continue

        values.setdefault(amount, []).append(field)

    duplicates = []

    for names in values.values():
        if len(names) > 1:
            duplicates.extend(names)

    return duplicates


def _to_float(value: Any) -> float | None:
    if value is None:
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None