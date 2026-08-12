import streamlit as st

from app import (
    apply_theme,
    page_header,
    render_footer,
    render_prediction_result,
    render_sidebar,
    save_uploaded_file,
)
from inference.image_detector import predict_ai_image

st.set_page_config(
    page_title="AI Generated Image Detection | VeriShield AI",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
render_sidebar()

page_header(
    "AI Generated Image Detection",
    (
        "Upload an image to detect whether it is real or AI-generated using "
        "deep learning and Grad-CAM evidence."
    ),
)

uploaded_file = st.file_uploader(
    "Upload image",
    type=["jpg", "jpeg", "png", "bmp", "webp"],
    key="module1_uploader",
)

if uploaded_file:
    # Only save a new copy when this is a genuinely different upload -
    # otherwise every rerun (e.g. clicking the button below) would write
    # another duplicate file into outputs/temp.
    if st.session_state.get("module1_uploaded_name") != uploaded_file.name:
        st.session_state["module1_image_path"] = save_uploaded_file(uploaded_file)
        st.session_state["module1_uploaded_name"] = uploaded_file.name
        # A new file was uploaded, so any previous result is now stale.
        st.session_state.pop("module1_result", None)

    image_path = st.session_state["module1_image_path"]

    left, right = st.columns([0.9, 1.1], gap="large")

    with left:
        st.markdown("### Uploaded Image")
        st.image(str(image_path), width="stretch")

    with right:
        st.markdown("### Analysis")
        st.markdown(
            """
            <div class="soft-card">
                <p>
                    This module checks whether the uploaded image is real or AI-generated.
                    It returns prediction, confidence, risk level, Grad-CAM, JSON report,
                    and PDF report.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Run AI Image Detection", width="stretch", type="primary"):
            with st.spinner("Loading model and analyzing image..."):
                try:
                    st.session_state["module1_result"] = predict_ai_image(image_path)
                except Exception as error:
                    st.session_state.pop("module1_result", None)
                    st.error("AI image detection failed.")
                    st.exception(error)

if "module1_result" in st.session_state:
    st.markdown("---")
    render_prediction_result(st.session_state["module1_result"])

render_footer()