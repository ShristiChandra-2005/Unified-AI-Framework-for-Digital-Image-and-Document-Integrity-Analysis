from pathlib import Path
from typing import Any
from uuid import uuid4

import streamlit as st


APP_TITLE = "VeriShield AI"
APP_SUBTITLE = "Enterprise Digital Fraud Detection & Integrity Platform"

BASE_DIR = Path(__file__).resolve().parent
TEMP_DIR = BASE_DIR / "outputs" / "temp"
REPORTS_DIR = BASE_DIR / "outputs" / "reports"

TEMP_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def apply_theme() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        [data-testid="stSidebarNav"],
        [data-testid="stSidebarNavItems"],
        [data-testid="stSidebarNavSeparator"],
        div[data-testid="stSidebarNav"] {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            min-height: 0 !important;
            max-height: 0 !important;
            overflow: hidden !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        header[data-testid="stHeader"] {
            background: transparent;
        }

        :root {
            --bg: #101827;
            --panel: #172235;
            --teal: #14B8A6;
            --blue: #38BDF8;
            --gold: #FBBF24;
            --red: #F87171;
            --green: #34D399;
            --text: #F8FAFC;
            --muted: #CBD5E1;
            --soft: #94A3B8;
            --border: rgba(255,255,255,0.13);
        }

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(20,184,166,0.14), transparent 28%),
                radial-gradient(circle at top right, rgba(56,189,248,0.12), transparent 30%),
                linear-gradient(135deg, #101827 0%, #122033 50%, #0F2A35 100%);
            color: var(--text);
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1160px;
        }

        section[data-testid="stSidebar"] {
            background: #0B1220;
            border-right: 1px solid var(--border);
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 1.2rem;
        }

        h1, h2, h3, h4, p, span, label {
            color: var(--text);
        }

        .brand {
            padding: 1rem 0.75rem 1.2rem;
            border-bottom: 1px solid var(--border);
            margin-bottom: 1rem;
        }

        .brand-title {
            font-size: 1.18rem;
            font-weight: 800;
        }

        .brand-subtitle {
            color: var(--muted);
            font-size: 0.78rem;
            line-height: 1.45;
            margin-top: 0.35rem;
        }

        .hero {
            background:
                linear-gradient(135deg, rgba(29,43,66,0.96), rgba(18,49,58,0.94));
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 2.5rem;
            box-shadow: 0 18px 48px rgba(0,0,0,0.26);
            margin-bottom: 1.8rem;
        }

        .eyebrow {
            display: inline-flex;
            color: #A7F3D0;
            background: rgba(20,184,166,0.13);
            border: 1px solid rgba(20,184,166,0.38);
            border-radius: 999px;
            padding: 0.38rem 0.75rem;
            font-size: 0.72rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 1rem;
        }

        .hero h1 {
            font-size: 2.5rem;
            line-height: 1.08;
            font-weight: 800;
            margin-bottom: 0.85rem;
        }

        .hero p {
            color: var(--muted);
            line-height: 1.65;
            font-size: 1rem;
            max-width: 900px;
        }

        .soft-card,
        .metric-card {
            background: rgba(29,43,66,0.88);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.15rem;
            box-shadow: 0 14px 38px rgba(0,0,0,0.18);
        }

        .module-card {
            background: rgba(29,43,66,0.90);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.25rem;
            min-height: 265px;
            height: 265px;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            box-shadow: 0 14px 38px rgba(0,0,0,0.18);
            transition: transform 0.18s ease, border-color 0.18s ease, background 0.18s ease;
        }

        .module-card:hover {
            transform: translateY(-5px);
            border-color: rgba(20,184,166,0.70);
            background: rgba(32,49,74,0.96);
        }

        .module-tag {
            color: #A7F3D0;
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            margin-bottom: 1rem;
        }

        .module-card h3 {
            font-size: 1.22rem;
            line-height: 1.28;
            margin-bottom: 1rem;
        }

        .module-card p,
        .soft-card p {
            color: var(--muted);
            line-height: 1.6;
            font-size: 0.94rem;
        }

        .metric-card {
            min-height: 108px;
            margin-bottom: 0.75rem;
        }

        .metric-label {
            color: var(--soft);
            font-size: 0.74rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .metric-value {
            font-size: 1.35rem;
            font-weight: 800;
            margin-top: 0.25rem;
        }

        .metric-caption {
            color: var(--muted);
            font-size: 0.82rem;
            margin-top: 0.25rem;
            line-height: 1.4;
        }

        .badge {
            display: inline-flex;
            border-radius: 999px;
            padding: 0.4rem 0.75rem;
            font-weight: 800;
            font-size: 0.78rem;
            text-transform: uppercase;
        }

        .badge-low {
            color: #86EFAC;
            background: rgba(52,211,153,0.14);
            border: 1px solid rgba(52,211,153,0.36);
        }

        .badge-medium {
            color: #FDE68A;
            background: rgba(251,191,36,0.14);
            border: 1px solid rgba(251,191,36,0.36);
        }

        .badge-high {
            color: #FCA5A5;
            background: rgba(248,113,113,0.14);
            border: 1px solid rgba(248,113,113,0.36);
        }

        .summary-list li {
            margin-bottom: 0.45rem;
            color: var(--muted);
        }

        .workflow-step {
            text-align: center;
            padding: 1rem;
            border-radius: 14px;
            background: rgba(29,43,66,0.88);
            border: 1px solid var(--border);
            font-weight: 800;
            min-height: 58px;
        }

        .footer {
            border-top: 1px solid var(--border);
            margin-top: 2.5rem;
            padding-top: 1rem;
            color: var(--soft);
            font-size: 0.82rem;
            line-height: 1.55;
        }

        .footer b {
            color: var(--text);
        }

        .stButton > button,
        .stLinkButton > a {
            border-radius: 12px !important;
            background: linear-gradient(135deg, var(--teal), var(--blue)) !important;
            color: #06121F !important;
            border: 0 !important;
            font-weight: 800 !important;
            min-height: 2.7rem !important;
            transition: 0.18s ease !important;
            text-decoration: none !important;
        }

        .stButton > button:hover,
        .stLinkButton > a:hover {
            transform: translateY(-2px);
            filter: brightness(1.08);
        }

        .stDownloadButton > button {
            border-radius: 12px;
            border: 1px solid var(--border);
            background: rgba(255,255,255,0.05);
            color: var(--text);
            font-weight: 700;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="hero">
            <div class="eyebrow">Enterprise AI Integrity Platform</div>
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def nav_button(label: str, url_path: str) -> None:
    st.link_button(label, url_path, width="stretch")


def action_button(label: str, url_path: str) -> None:
    st.link_button(label, url_path, width="stretch")


def metric_card(label: str, value: Any, caption: str = "") -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-caption">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_badge(label: str, status: str | None = None) -> None:
    level = (status or label or "medium").lower()
    css_class = "badge-medium"

    if "low" in level or "trusted" in level or "pass" in level or "ready" in level:
        css_class = "badge-low"
    elif "high" in level or "fail" in level or "tampered" in level or "fake" in level:
        css_class = "badge-high"

    st.markdown(
        f'<span class="badge {css_class}">{label}</span>',
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown(
            """
            <div class="brand">
                <div class="brand-title">VeriShield AI</div>
                <div class="brand-subtitle">
                    Enterprise Digital Fraud Detection & Integrity Platform
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        nav_button("Home", "/")
        nav_button("Start Analysis", "/Start_Analysis")
        nav_button("AI Image Detection", "/AI_Generated_Image_Detection")
        nav_button("Receipt Verification", "/Receipt_Verification")
        nav_button("Image Tampering Detection", "/Image_Tampering_Detection")
        nav_button("About", "/About")
        nav_button("Admin Login", "/admin_login")

        if st.session_state.get("is_admin"):
            nav_button("Admin Dashboard", "/Admin_Dashboard")

        st.markdown("---")
        st.markdown(
            """
            <div class="soft-card">
                <b>VeriShield AI</b><br>
                <span style="color:#CBD5E1;font-size:0.78rem;">
                    Version 1.0<br>
                    Developed by <b>Shristi Chandra</b><br>
                    B.Tech CSE-AI, IGDTUW
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_footer() -> None:
    st.markdown(
        """
        <div class="footer">
            <div><b>VeriShield AI</b></div>
            <div>Enterprise Digital Fraud Detection & Integrity Platform</div>
            <div>
                Version 1.0 | Developed by <b>Shristi Chandra</b> |
                B.Tech CSE-AI, IGDTUW | 2026
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def save_uploaded_file(uploaded_file, target_dir: Path = TEMP_DIR) -> Path:
    target_dir.mkdir(parents=True, exist_ok=True)

    suffix = Path(uploaded_file.name).suffix.lower()
    safe_stem = Path(uploaded_file.name).stem.replace(" ", "_")
    path = target_dir / f"{safe_stem}_{uuid4().hex[:8]}{suffix}"

    path.write_bytes(uploaded_file.getbuffer())
    return path


def read_report_file(report_path: str | Path | None) -> bytes | None:
    if not report_path:
        return None

    path = Path(report_path)

    if not path.exists():
        return None

    return path.read_bytes()


def render_downloads(result: dict[str, Any]) -> None:
    report_path = result.get("report_path") or result.get("report", {}).get("json")
    pdf_path = result.get("pdf_report_path") or result.get("report", {}).get("pdf")

    report_bytes = read_report_file(report_path)
    pdf_bytes = read_report_file(pdf_path)

    col1, col2 = st.columns(2)

    with col1:
        if report_bytes:
            st.download_button(
                "Download JSON Report",
                data=report_bytes,
                file_name=Path(report_path).name,
                mime="application/json",
                width="stretch",
            )
        else:
            st.button("JSON Report Not Available", disabled=True, width="stretch")

    with col2:
        if pdf_bytes:
            st.download_button(
                "Download PDF Report",
                data=pdf_bytes,
                file_name=Path(pdf_path).name,
                mime="application/pdf",
                width="stretch",
            )
        else:
            st.button("PDF Report Not Available", disabled=True, width="stretch")


def render_summary(summary: Any) -> None:
    if not summary:
        return

    if isinstance(summary, str):
        st.markdown("### Decision Summary")
        st.info(summary)
        return

    if isinstance(summary, dict):
        title = summary.get("title") or "Decision Summary"
        points = summary.get("summary") or summary.get("points") or []
        recommendation = summary.get("recommendation")

        st.markdown(f"### {title}")

        if isinstance(points, str):
            st.info(points)
        elif isinstance(points, list):
            html = "<ul class='summary-list'>"
            for point in points:
                html += f"<li>{point}</li>"
            html += "</ul>"
            st.markdown(html, unsafe_allow_html=True)

        if recommendation:
            st.info(recommendation)

        return

    if isinstance(summary, list):
        st.markdown("### Decision Summary")
        html = "<ul class='summary-list'>"
        for point in summary:
            html += f"<li>{point}</li>"
        html += "</ul>"
        st.markdown(html, unsafe_allow_html=True)


def render_prediction_result(result: dict[str, Any]) -> None:
    if not result.get("success"):
        st.error(result.get("error", "Analysis failed."))
        return

    module = result.get("module", "")

    if module == "Module 2 - Receipt Verification" or result.get("receipt_status"):
        render_receipt_result(result)
        return

    if module == "Module 3 - Image Tampering Detection":
        render_tampering_result(result)
        return

    render_ai_image_result(result)


def render_ai_image_result(result: dict[str, Any]) -> None:
    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card("Prediction", result.get("prediction", "N/A"), "REAL / FAKE")

    with col2:
        metric_card(
            "Confidence",
            f"{result.get('confidence', 'N/A')}%",
            result.get("confidence_label", ""),
        )

    with col3:
        metric_card("Risk Score", result.get("risk_score", "N/A"), result.get("risk_level", ""))

    status_badge(f"{result.get('risk_level', 'Unknown')} Risk", result.get("risk_level"))
    render_summary(result.get("decision_summary"))
    _render_processing_table(result)
    _render_visualization(result, title="Grad-CAM Explainability")
    render_downloads(result)


def render_receipt_result(result: dict[str, Any]) -> None:
    receipt = result.get("receipt", {}) or result.get("fields", {})
    validation = result.get("validation", {})
    integrity = result.get("integrity", {})

    integrity_score = (
        integrity.get("integrity_score")
        or result.get("integrity_score")
        or result.get("confidence")
        or "N/A"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card(
            "Receipt Status",
            result.get("receipt_status", result.get("prediction", "N/A")),
            "Trusted / Suspicious / Manipulated",
        )

    with col2:
        metric_card("Integrity Score", f"{integrity_score}%", "OCR + metadata validation")

    with col3:
        metric_card(
            "Validation",
            result.get("validation_status", validation.get("status", "N/A")),
            "Rule-based verification",
        )

    st.markdown("### Receipt Fields")
    st.dataframe(
        {
            "Field": [
                "Merchant",
                "Invoice Number",
                "Invoice Date",
                "Subtotal",
                "Tax",
                "Total Amount",
                "Currency",
                "Phone",
                "Address",
            ],
            "Value": [
                receipt.get("merchant") or result.get("merchant") or "Not detected",
                receipt.get("invoice_number") or result.get("invoice_number") or "Not detected",
                receipt.get("date") or result.get("invoice_date") or "Not detected",
                receipt.get("subtotal") or result.get("subtotal") or "N/A",
                receipt.get("tax") or result.get("tax") or "N/A",
                receipt.get("total") or result.get("total_amount") or "Not detected",
                receipt.get("currency") or result.get("currency") or "N/A",
                receipt.get("phone") or result.get("phone") or "N/A",
                receipt.get("address") or result.get("address") or "N/A",
            ],
        },
        width="stretch",
        hide_index=True,
    )

    st.markdown("### Metadata Validation")

    validation_checks = result.get("validation_checks") or [
        {"Check": "Merchant Found", "Result": "Passed" if validation.get("merchant_found") else "Review Needed"},
        {"Check": "Invoice Found", "Result": "Passed" if validation.get("invoice_found") else "Review Needed"},
        {"Check": "Date Valid", "Result": "Passed" if validation.get("date_valid") else "Review Needed"},
        {"Check": "Amount Valid", "Result": "Passed" if validation.get("amount_valid") else "Review Needed"},
        {"Check": "Tax Consistent", "Result": "Passed" if validation.get("tax_consistent") else "Review Needed"},
    ]

    st.dataframe(validation_checks, width="stretch", hide_index=True)

    ocr = result.get("ocr", {})
    detected_text = ocr.get("detected_text") or ocr.get("text")

    if detected_text:
        st.markdown("### OCR Text")
        st.text_area("Detected Text", value=detected_text, height=220, disabled=True)

    render_summary(result.get("decision_summary"))
    _render_processing_table(result)
    render_downloads(result)


def render_tampering_result(result: dict[str, Any]) -> None:
    details = result.get("details", {})

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card("Prediction", result.get("prediction", "N/A"), "Authentic / Tampered")

    with col2:
        metric_card(
            "Confidence",
            f"{result.get('confidence', 'N/A')}%",
            result.get("confidence_label", ""),
        )

    with col3:
        metric_card("Risk Score", result.get("risk_score", "N/A"), result.get("risk_level", ""))

    st.markdown("### Forensic Details")
    st.dataframe(
        {
            "Property": [
                "Tampering Type",
                "Affected Region",
                "Localization Status",
                "Heatmap Status",
                "Recommendation",
            ],
            "Value": [
                details.get("tampering_type", result.get("tampering_type", "N/A")),
                details.get("affected_region", result.get("affected_region", "N/A")),
                details.get("localization_status", result.get("localization_status", "N/A")),
                details.get("heatmap_status", result.get("heatmap_status", "N/A")),
                details.get("recommendation", result.get("recommendation", "Manual verification recommended.")),
            ],
        },
        width="stretch",
        hide_index=True,
    )

    status_badge(f"{result.get('risk_level', 'Unknown')} Risk", result.get("risk_level"))
    render_summary(result.get("decision_summary"))
    _render_processing_table(result)
    _render_visualization(result, title="Tampering Heatmap")
    render_downloads(result)


def _render_processing_table(result: dict[str, Any]) -> None:
    processing = result.get("processing", {})

    st.markdown("### Processing Details")
    st.dataframe(
        {
            "Property": ["Processing Time", "Device", "Timestamp"],
            "Value": [
                f"{result.get('processing_time_ms') or processing.get('time_ms', 'N/A')} ms",
                result.get("device") or processing.get("device", "N/A"),
                result.get("timestamp") or processing.get("timestamp", "N/A"),
            ],
        },
        width="stretch",
        hide_index=True,
    )


def _render_visualization(result: dict[str, Any], title: str) -> None:
    visualization = result.get("visualization", {})

    visual_path = (
        result.get("visualization_path")
        or result.get("gradcam_path")
        or result.get("heatmap_path")
        or visualization.get("overlay")
        or visualization.get("gradcam")
        or visualization.get("heatmap")
    )

    if visual_path and Path(visual_path).exists():
        st.markdown(f"### {title}")
        st.image(str(visual_path), caption=title, width="stretch")
        return

    error = visualization.get("error") or result.get("visualization_error")
    if error and error != "N/A":
        st.warning(f"{title} unavailable: {error}")


def render_start_analysis() -> None:
    st.markdown("## Choose Analysis Module")

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown(
            """
            <div class="module-card">
                <div class="module-tag">Module 1</div>
                <h3>AI Generated Image Detection</h3>
                <p>
                    Detect whether an uploaded image is real or AI-generated.
                    Includes confidence, risk level, and Grad-CAM explainability.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        action_button("Open AI Detection", "/AI_Generated_Image_Detection")

    with col2:
        st.markdown(
            """
            <div class="module-card">
                <div class="module-tag">Module 2</div>
                <h3>Receipt Verification</h3>
                <p>
                    Extract receipt text, detect merchant and invoice fields,
                    validate metadata, and calculate an integrity score.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        action_button("Open Receipt Verification", "/Receipt_Verification")

    with col3:
        st.markdown(
            """
            <div class="module-card">
                <div class="module-tag">Module 3</div>
                <h3>Image Tampering Detection</h3>
                <p>
                    Detect manipulated images and show forensic heatmap evidence
                    for suspicious image regions.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        action_button("Open Tampering Detection", "/Image_Tampering_Detection")


def render_module_cards() -> None:
    render_start_analysis()


def render_workflow() -> None:
    st.markdown("## Workflow")

    cols = st.columns(6)
    steps = ["Upload", "Preprocess", "AI / OCR", "Risk", "JSON", "PDF"]

    for col, step in zip(cols, steps):
        with col:
            st.markdown(f"<div class='workflow-step'>{step}</div>", unsafe_allow_html=True)


def render_home() -> None:
    apply_theme()
    render_sidebar()

    page_header(
        "VeriShield AI",
        (
            "Enterprise Digital Fraud Detection Platform. Detect, verify, and protect "
            "digital images and documents using deep learning, OCR, explainability, "
            "and structured reporting."
        ),
    )

    left, right = st.columns([1.35, 0.65], gap="large")

    with left:
        st.markdown(
            """
            <div class="soft-card">
                <h3>Digital Fraud Detection in One Platform</h3>
                <p>
                    VeriShield AI brings together AI-generated image detection,
                    receipt verification, image tampering detection, visual evidence,
                    integrity scoring, JSON reports, and PDF reports in one
                    professional research-grade system.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        action_button("Start Analysis", "/Start_Analysis")

    with right:
        metric_card("Detection Modules", "3", "Images, receipts, tampering")
        metric_card("Deep Learning", "Ready", "Module 1 and Module 3")
        metric_card("Reports", "JSON + PDF", "Download-ready evidence")

    st.markdown("## Platform Capabilities")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card("AI Image", "REAL / FAKE", "EfficientNet + Grad-CAM")

    with c2:
        metric_card("Receipt", "Integrity", "OCR + metadata validation")

    with c3:
        metric_card("Tampering", "Heatmap", "Forensic localization")

    with c4:
        metric_card("Admin", "Dashboard", "Report analytics")

    render_start_analysis()
    render_workflow()

    st.markdown("## Technology Stack")
    st.dataframe(
        {
            "Layer": [
                "Deep Learning",
                "OCR",
                "Computer Vision",
                "Frontend",
                "Reporting",
                "Language",
            ],
            "Technology": [
                "PyTorch, EfficientNet",
                "EasyOCR",
                "OpenCV, Grad-CAM",
                "Streamlit",
                "JSON, PDF, ReportLab",
                "Python",
            ],
        },
        width="stretch",
        hide_index=True,
    )

    st.markdown("## Research Highlights")
    st.markdown(
        """
        <div class="soft-card">
            <p>
                The platform demonstrates a unified integrity workflow across
                generated images, receipt documents, and tampered visuals. Each
                module returns a module-specific decision, risk assessment,
                evidence visualization where applicable, and reproducible reports.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_footer()


if __name__ == "__main__":
    st.set_page_config(
        page_title=f"{APP_TITLE} | Home",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    render_home()