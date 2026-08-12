import json
from collections import Counter
from pathlib import Path
from typing import Any

import pandas as pd
import plotly.express as px
import streamlit as st

from app import (
    REPORTS_DIR,
    apply_theme,
    metric_card,
    page_header,
    render_footer,
    render_sidebar,
)


MODULE_AI = "Module 1 - AI Generated Image Detection"
MODULE_RECEIPT = "Module 2 - Receipt Verification"
MODULE_TAMPERING = "Module 3 - Image Tampering Detection"


def load_reports() -> list[dict[str, Any]]:
    reports: list[dict[str, Any]] = []

    if not REPORTS_DIR.exists():
        return reports

    for path in sorted(REPORTS_DIR.glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            data["_json_file"] = str(path)
            data["_pdf_file"] = data.get("pdf_report_path") or data.get("report", {}).get("pdf")
            reports.append(data)
        except (json.JSONDecodeError, OSError):
            continue

    return reports


def _safe_number(value: Any) -> float | None:
    """Coerce a report value to float for a NUMERIC dataframe column.

    This used to return the string "N/A" when conversion failed, which
    mixed floats and strings in the same pandas column - exactly what
    crashed Streamlit's Arrow conversion with:
    "Could not convert 'N/A' with type str: tried to convert to double".

    Returning None instead lets pandas represent the gap as NaN, which
    Arrow handles natively in a float column. "N/A" is only for display
    text (via format_display_number below), never inside a numeric
    dataframe column.
    """
    try:
        return round(float(value), 2)
    except (TypeError, ValueError):
        return None


def format_display_number(value: float | None, suffix: str = "") -> str:
    """Presentation-only formatting for metric_card()/text - not for dataframes."""
    if value is None:
        return "N/A"
    return f"{value}{suffix}"


def build_report_dataframe(reports: list[dict[str, Any]]) -> pd.DataFrame:
    rows = []

    for report in reports:
        module = report.get("module", "Unknown")
        confidence = report.get("confidence")
        processing_time = (
            report.get("processing_time_ms")
            or report.get("processing_time")
            or report.get("processing", {}).get("time_ms")
        )

        rows.append(
            {
                "Module": module,
                "Result": _module_result(report),
                "Confidence / Score": _safe_number(confidence),
                "Risk Level": report.get("risk_level", "N/A"),
                "Status": report.get("status", "N/A"),
                "Processing Time (ms)": _safe_number(processing_time),
                "Timestamp": report.get("timestamp") or report.get("generated_time") or "N/A",
                "JSON Report": report.get("_json_file"),
                "PDF Report": report.get("_pdf_file"),
            }
        )

    df = pd.DataFrame(rows)

    # Belt-and-suspenders: even if something upstream ever slips a stray
    # string into one of these two columns again, force them back to a
    # clean numeric dtype (bad values become NaN, not a crash) before any
    # dataframe in this file ever gets displayed.
    if not df.empty:
        df["Confidence / Score"] = pd.to_numeric(df["Confidence / Score"], errors="coerce")
        df["Processing Time (ms)"] = pd.to_numeric(df["Processing Time (ms)"], errors="coerce")

    return df


def _module_result(report: dict[str, Any]) -> str:
    module = report.get("module", "")

    if module == MODULE_RECEIPT:
        return str(report.get("receipt_status") or report.get("prediction") or "N/A")

    if module == MODULE_TAMPERING:
        return str(report.get("prediction") or "N/A")

    return str(report.get("prediction") or "N/A")


def render_admin_guard() -> bool:
    if st.session_state.get("is_admin"):
        return True

    st.error("Access Denied. Please login first.")
    st.info("Admin authentication is required to view report analytics.")

    if st.button("Go to Admin Login", width="stretch"):
        st.switch_page("pages/8_admin_login.py")

    return False


st.set_page_config(
    page_title="Admin Dashboard | VeriShield AI",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
render_sidebar()

page_header(
    "Admin Dashboard",
    "Enterprise monitoring view for report history, module usage, risk trends, processing time, and generated JSON/PDF evidence.",
)

if not render_admin_guard():
    render_footer()
    st.stop()

reports = load_reports()
df = build_report_dataframe(reports)

total_reports = len(reports)
module_counts = Counter(report.get("module", "Unknown") for report in reports)
risk_counts = Counter(report.get("risk_level", "Unknown") for report in reports)

avg_confidence = (
    round(df["Confidence / Score"].dropna().mean(), 2)
    if not df.empty and not df["Confidence / Score"].dropna().empty
    else None
)
avg_processing = (
    round(df["Processing Time (ms)"].dropna().mean(), 2)
    if not df.empty and not df["Processing Time (ms)"].dropna().empty
    else None
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card("Total Analyses", total_reports, "Generated JSON reports")

with col2:
    metric_card(
        "Avg Confidence / Score",
        format_display_number(avg_confidence),
        "Across available reports",
    )

with col3:
    metric_card(
        "Avg Processing Time",
        format_display_number(avg_processing, " ms"),
        "Backend inference time",
    )

with col4:
    metric_card("PDF Reports", sum(1 for report in reports if report.get("_pdf_file")), "Generated PDF evidence")

st.markdown("## Module Usage")

m1, m2, m3 = st.columns(3)

with m1:
    metric_card(
        "AI Image Detection",
        module_counts.get(MODULE_AI, 0),
        "Module 1 reports",
    )

with m2:
    metric_card(
        "Receipt Verification",
        module_counts.get(MODULE_RECEIPT, 0),
        "Module 2 reports",
    )

with m3:
    metric_card(
        "Image Tampering",
        module_counts.get(MODULE_TAMPERING, 0),
        "Module 3 reports",
    )

if df.empty:
    st.info("No reports found yet. Run analyses from the module pages first.")
    render_footer()
    st.stop()

left, right = st.columns(2, gap="large")

with left:
    st.markdown("### Risk Distribution")
    risk_df = pd.DataFrame(
        {
            "Risk Level": list(risk_counts.keys()),
            "Count": list(risk_counts.values()),
        }
    )

    fig = px.pie(
        risk_df,
        names="Risk Level",
        values="Count",
        hole=0.55,
        color="Risk Level",
        color_discrete_map={
            "Low": "#10B981",
            "Medium": "#F59E0B",
            "High": "#EF4444",
            "N/A": "#64748B",
            "Unknown": "#64748B",
        },
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=10, b=0),
    )
    st.plotly_chart(fig, width="stretch")

with right:
    st.markdown("### Module Usage")
    module_df = pd.DataFrame(
        {
            "Module": list(module_counts.keys()),
            "Count": list(module_counts.values()),
        }
    )

    fig = px.bar(
        module_df,
        x="Module",
        y="Count",
        color="Module",
        color_discrete_sequence=["#2563EB", "#0EA5E9", "#10B981"],
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=10, b=0),
        showlegend=False,
    )
    st.plotly_chart(fig, width="stretch")

left, right = st.columns(2, gap="large")

with left:
    st.markdown("### Confidence / Integrity Score Trend")
    trend_df = df.dropna(subset=["Confidence / Score"])

    if trend_df.empty:
        st.info("No numeric confidence values available yet.")
    else:
        fig = px.line(
            trend_df.iloc[::-1],
            y="Confidence / Score",
            color="Module",
            markers=True,
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0),
        )
        st.plotly_chart(fig, width="stretch")

with right:
    st.markdown("### Processing Time")
    time_df = df.dropna(subset=["Processing Time (ms)"])

    if time_df.empty:
        st.info("No processing time values available yet.")
    else:
        fig = px.histogram(
            time_df,
            x="Processing Time (ms)",
            color="Module",
            nbins=12,
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0),
        )
        st.plotly_chart(fig, width="stretch")

st.markdown("## Recent Reports")

display_df = df[
    [
        "Timestamp",
        "Module",
        "Result",
        "Confidence / Score",
        "Risk Level",
        "Status",
        "Processing Time (ms)",
        "JSON Report",
        "PDF Report",
    ]
].head(25)

st.dataframe(
    display_df,
    width="stretch",
    hide_index=True,
)

st.markdown("## Report Downloads")

selected_index = st.selectbox(
    "Select report",
    options=list(range(len(reports))),
    format_func=lambda index: (
        f"{df.iloc[index]['Timestamp']} | "
        f"{df.iloc[index]['Module']} | "
        f"{df.iloc[index]['Result']}"
    ),
)

selected_report = reports[selected_index]
json_path = Path(selected_report["_json_file"])
pdf_value = selected_report.get("_pdf_file")
pdf_path = Path(pdf_value) if pdf_value else None

download_col1, download_col2 = st.columns(2)

with download_col1:
    if json_path.exists():
        st.download_button(
            "Download Selected JSON",
            data=json_path.read_bytes(),
            file_name=json_path.name,
            mime="application/json",
            width="stretch",
        )
    else:
        st.button("JSON Not Available", disabled=True, width="stretch")

with download_col2:
    if pdf_path and pdf_path.exists():
        st.download_button(
            "Download Selected PDF",
            data=pdf_path.read_bytes(),
            file_name=pdf_path.name,
            mime="application/pdf",
            width="stretch",
        )
    else:
        st.button("PDF Not Available", disabled=True, width="stretch")

render_footer()