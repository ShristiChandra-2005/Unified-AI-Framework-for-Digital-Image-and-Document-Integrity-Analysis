import streamlit as st

from app import (
    apply_theme,
    page_header,
    render_footer,
    render_prediction_result,
    render_sidebar,
    save_uploaded_file,
)
from inference.tampering_detector import predict_tampering

apply_theme()
render_sidebar()

page_header(
    "Image Tampering Detection",
    "Upload an image to detect manipulation and generate Grad-CAM forensic localization evidence.",
)

uploaded_file = st.file_uploader(
    "Upload image",
    type=["jpg", "jpeg", "png", "bmp", "webp"],
    key="module3_uploader",
)

if uploaded_file:
    # Only save a new copy when this is a genuinely different upload -
    # otherwise every rerun (e.g. clicking the button below) would write
    # another duplicate file into outputs/temp.
    if st.session_state.get("module3_uploaded_name") != uploaded_file.name:
        st.session_state["module3_image_path"] = save_uploaded_file(uploaded_file)
        st.session_state["module3_uploaded_name"] = uploaded_file.name
        # A new file was uploaded, so any previous result is now stale.
        st.session_state.pop("module3_result", None)

    image_path = st.session_state["module3_image_path"]

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
                    It returns prediction, confidence, risk level, Grad-CAM forensic
                    localization, JSON report, and PDF report.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Run Tampering Detection", width="stretch", type="primary"):
            with st.spinner("Loading model and generating Grad-CAM localization..."):
                try:
                    st.session_state["module3_result"] = predict_tampering(image_path)
                except Exception as error:
                    st.session_state.pop("module3_result", None)
                    st.error("Image tampering detection failed.")
                    st.exception(error)

if "module3_result" in st.session_state:
    st.markdown("---")
    render_prediction_result(st.session_state["module3_result"])

render_footer()
