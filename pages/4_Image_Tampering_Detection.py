import streamlit as st

from app import (
    apply_theme,
    page_header,
    render_footer,
    render_prediction_result,
    render_sidebar,
    save_uploaded_file,
)

st.set_page_config(
    page_title="Image Tampering Detection | VeriShield AI",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
render_sidebar()

page_header(
    "Image Tampering Detection",
    "Upload an image to detect manipulation and generate forensic heatmap evidence.",
)

uploaded_file = st.file_uploader(
    "Upload image",
    type=["jpg", "jpeg", "png", "bmp", "webp"],
)

if uploaded_file:
    image_path = save_uploaded_file(uploaded_file)

    left, right = st.columns([0.9, 1.1], gap="large")

    with left:
        st.markdown("### Uploaded Image")
        st.image(str(image_path), width="stretch")

    with right:
        st.markdown("### Detection")
        st.markdown(
            """
            <div class="soft-card">
                <p>
                    This module detects whether the image is authentic or tampered.
                    It returns prediction, confidence, risk level, heatmap evidence,
                    JSON report, and PDF report.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Run Tampering Detection", width="stretch"):
            with st.spinner("Loading model and analyzing tampering evidence..."):
                try:
                    from inference.tampering_detector import predict_tampering

                    st.session_state["module3_result"] = predict_tampering(image_path)

                except Exception as error:
                    st.error("Image tampering detection failed.")
                    st.exception(error)

if "module3_result" in st.session_state:
    st.markdown("---")
    render_prediction_result(st.session_state["module3_result"])

render_footer()
