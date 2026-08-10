import streamlit as st

from app import apply_theme, metric_card, page_header, render_footer, render_sidebar


st.set_page_config(
    page_title="About",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
render_sidebar()

page_header(
    "About the Project",
    "A research-oriented AI framework for digital image and document integrity analysis.",
)

st.markdown("## Project Title")
st.markdown(
    """
    Unified AI Framework for Digital Fraud Detection using Deep Learning, OCR,
    Explainable AI, Metadata Validation, and Risk Analysis.
    """
)

st.markdown("## Problem Statement")
st.markdown(
    """
    Digital fraud is increasing through AI-generated images, manipulated visual
    evidence, and forged receipts. This project builds a unified framework to
    detect, verify, explain, and report suspicious digital content.
    """
)

st.markdown("## Objectives")
st.markdown(
    """
    - Detect AI-generated images using deep learning.
    - Verify receipts using OCR, field extraction, metadata validation, and integrity scoring.
    - Detect image tampering using deep learning and Grad-CAM.
    - Provide structured JSON reports for reproducible analysis.
    - Build a professional Streamlit dashboard for demonstration and deployment.
    """
)

st.markdown("## Modules")

col1, col2, col3 = st.columns(3)

with col1:
    metric_card(
        "Module 1",
        "AI Image Detection",
        "CIFAKE based real vs AI-generated image classification",
    )

with col2:
    metric_card(
        "Module 2",
        "Receipt Verification",
        "SROIE/CORD OCR and metadata validation",
    )

with col3:
    metric_card(
        "Module 3",
        "Tampering Detection",
        "CASIA v2 and IMD2020 image manipulation detection",
    )

st.markdown("## Technology Stack")
st.markdown(
    """
    - Python
    - Streamlit
    - PyTorch
    - Torchvision
    - EasyOCR
    - OpenCV
    - Plotly
    - Grad-CAM
    - JSON reporting
    """
)

st.markdown("## Developer")
st.markdown(
    """
    **Developed by Shristi Chandra**  
    B.Tech Major Project and Research Portfolio System
    """
)

st.markdown("## Future Scope")
st.markdown(
    """
    - PDF report generation.
    - Batch processing.
    - Cloud deployment.
    - Database-backed report history.
    - More forensic datasets and advanced explainability.
    """
)

render_footer()
