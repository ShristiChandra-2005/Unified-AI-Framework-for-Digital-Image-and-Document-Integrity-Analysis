import re
from typing import Any


TOTAL_KEYWORDS = ["grand total", "net total", "amount due", "total", "balance"]
SUBTOTAL_KEYWORDS = ["subtotal", "sub total", "sub-total", "before tax"]
TAX_KEYWORDS = ["tax", "gst", "vat", "service tax", "sst"]
INVOICE_KEYWORDS = ["invoice", "inv", "bill", "receipt", "order", "transaction"]


def extract_receipt_fields(text: str) -> dict[str, Any]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    joined_text = "\n".join(lines)

    fields = {
        "merchant": _extract_merchant(lines),
        "date": _extract_date(joined_text),
        "invoice_number": _extract_invoice_number(lines),
        "subtotal": _extract_amount_by_keywords(lines, SUBTOTAL_KEYWORDS),
        "tax": _extract_amount_by_keywords(lines, TAX_KEYWORDS),
        "total": _extract_total_amount(lines),
        "currency": _extract_currency(joined_text),
        "phone": _extract_phone(joined_text),
        "address": _extract_address(lines),
    }

    detected = sum(1 for value in fields.values() if value not in [None, "", []])
    fields["field_confidence"] = round((detected / 9) * 100, 2)

    return fields


def _extract_merchant(lines: list[str]) -> str | None:
    ignored_keywords = [
        "receipt",
        "invoice",
        "tax invoice",
        "bill",
        "cash bill",
        "official receipt",
        "customer copy",
        "merchant copy",
        "date",
        "time",
        "total",
        "subtotal",
        "tax",
        "gst",
        "vat",
        "change",
        "cash",
        "card",
        "visa",
        "mastercard",
    ]

    for line in lines[:12]:
        clean_line = line.strip()
        lower_line = clean_line.lower()

        if not clean_line:
            continue

        if any(keyword in lower_line for keyword in ignored_keywords):
            continue

        if _contains_date(clean_line):
            continue

        if _contains_amount(clean_line):
            continue

        if _looks_like_phone(clean_line):
            continue

        if _looks_like_id(clean_line):
            continue

        if len(re.findall(r"[A-Za-z]", clean_line)) < 3:
            continue

        return clean_line

    fallback = [
        line for line in lines[:8]
        if len(re.findall(r"[A-Za-z]", line)) >= 3
    ]

    return fallback[0] if fallback else None


def _extract_date(text: str) -> str | None:
    patterns = [
        r"\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b",
        r"\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b",
        r"\b\d{1,2}\s+[A-Za-z]{3,9}\s+\d{2,4}\b",
        r"\b[A-Za-z]{3,9}\s+\d{1,2},?\s+\d{2,4}\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(0)

    return None


def _extract_invoice_number(lines: list[str]) -> str | None:
    for line in lines:
        lower_line = line.lower()

        if not any(keyword in lower_line for keyword in INVOICE_KEYWORDS):
            continue

        match = re.search(
            r"(invoice|inv|bill|receipt|order|transaction)\s*"
            r"(no|number|num|#|:|-)?\s*"
            r"([A-Za-z0-9][A-Za-z0-9/-]{2,})",
            line,
            re.IGNORECASE,
        )

        if match:
            value = match.group(3).strip()

            if _valid_invoice_value(value):
                return value

    for line in lines[:15]:
        match = re.search(
            r"\b[A-Z]{1,5}[-/]?\d{3,}[A-Z0-9/-]*\b|\b\d{6,}\b",
            line,
            re.IGNORECASE,
        )

        if match:
            value = match.group(0).strip()

            if _valid_invoice_value(value):
                return value

    return None


def _valid_invoice_value(value: str) -> bool:
    value = value.strip()

    if len(value) < 3:
        return False

    if value.lower() in {"oice", "voice", "number", "receipt", "invoice", "bill"}:
        return False

    return bool(re.search(r"\d", value))


def _extract_amount_by_keywords(lines: list[str], keywords: list[str]) -> float | None:
    candidates: list[float] = []

    for line in lines:
        lower_line = line.lower()

        if not any(keyword in lower_line for keyword in keywords):
            continue

        candidates.extend(_extract_amounts_from_line(line))

    return candidates[-1] if candidates else None


def _extract_total_amount(lines: list[str]) -> float | None:
    total_from_keyword = _extract_amount_by_keywords(lines, TOTAL_KEYWORDS)

    if total_from_keyword is not None:
        return total_from_keyword

    all_amounts: list[float] = []

    for line in lines:
        lower_line = line.lower()

        if _contains_date(line):
            continue

        if any(word in lower_line for word in ["phone", "tel", "mobile", "invoice", "receipt"]):
            continue

        if _looks_like_phone(line):
            continue

        all_amounts.extend(_extract_amounts_from_line(line))

    valid_amounts = [
        amount for amount in all_amounts
        if 0.01 <= amount <= 1_000_000
    ]

    return max(valid_amounts) if valid_amounts else None


def _extract_currency(text: str) -> str | None:
    match = re.search(r"\b(INR|USD|EUR|GBP|RM|Rs\.?)\b|[$]", text, re.IGNORECASE)

    if not match:
        return None

    value = match.group(0)

    if value == "$":
        return "USD"

    return value.upper().replace(".", "")


def _extract_phone(text: str) -> str | None:
    match = re.search(r"(\+?\d[\d\s-]{8,}\d)", text)

    if not match:
        return None

    phone = match.group(1).strip()
    digits = re.sub(r"\D", "", phone)

    if 9 <= len(digits) <= 15:
        return phone

    return None


def _extract_address(lines: list[str]) -> str | None:
    keywords = [
        "road",
        "street",
        "jalan",
        "lane",
        "shop",
        "city",
        "block",
        "sector",
        "market",
        "floor",
        "complex",
        "mall",
        "store",
    ]

    address_lines = [
        line for line in lines[:12]
        if any(keyword in line.lower() for keyword in keywords)
    ]

    if address_lines:
        return " ".join(address_lines[:3])

    meaningful = [
        line for line in lines[1:6]
        if not _contains_amount(line) and not _contains_date(line)
    ]

    return " ".join(meaningful[:3]) if meaningful else None


def _extract_amounts_from_line(line: str) -> list[float]:
    matches = re.findall(
        r"(?:INR|USD|RM|Rs\.?|\$)?\s*"
        r"([0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{1,2})?|[0-9]+(?:\.[0-9]{1,2})?)",
        line,
        re.IGNORECASE,
    )

    amounts: list[float] = []

    for match in matches:
        value = match.replace(",", "")

        try:
            amount = float(value)
        except ValueError:
            continue

        if amount > 0:
            amounts.append(amount)

    return amounts


def _contains_date(text: str) -> bool:
    return bool(
        re.search(
            r"\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b|"
            r"\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b",
            text,
        )
    )


def _contains_amount(text: str) -> bool:
    return bool(re.search(r"\d+\.\d{1,2}", text))


def _looks_like_phone(text: str) -> bool:
    digits = re.sub(r"\D", "", text)
    return 9 <= len(digits) <= 15


def _looks_like_id(text: str) -> bool:
    stripped = re.sub(r"[^A-Za-z0-9]", "", text)
    digits = re.findall(r"\d", stripped)
    letters = re.findall(r"[A-Za-z]", stripped)

    return len(stripped) >= 6 and len(digits) > len(letters)
