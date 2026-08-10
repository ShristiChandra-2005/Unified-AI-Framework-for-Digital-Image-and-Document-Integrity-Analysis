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
    page_title="Receipt Verification | VeriShield AI",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
render_sidebar()

page_header(
    "Receipt Verification",
    (
        "Extract OCR text, verify receipt fields, validate metadata, "
        "and calculate receipt integrity score."
    ),
)

st.info(
    "Module 2 uses EasyOCR and rule-based metadata validation. "
    "It does not use Grad-CAM, heatmap, or a trained image classifier."
)

uploaded_file = st.file_uploader(
    "Upload receipt image",
    type=["jpg", "jpeg", "png", "bmp", "webp"],
)

if uploaded_file:
    image_path = save_uploaded_file(uploaded_file)

    left, right = st.columns([0.9, 1.1], gap="large")

    with left:
        st.markdown("### Uploaded Receipt")
        st.image(str(image_path), width="stretch")

    with right:
        st.markdown("### Verification")
        st.markdown(
            """
            <div class="soft-card">
                <p>
                    The system will run OCR, extract merchant and invoice fields,
                    validate date and amount consistency, calculate integrity score,
                    and generate JSON/PDF reports.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Verify Receipt", width="stretch"):
            with st.spinner("Loading OCR engine and verifying receipt..."):
                try:
                    from inference.receipt_detector import verify_receipt

                    st.session_state["module2_result"] = verify_receipt(image_path)

                except Exception as error:
                    st.error("Receipt verification failed.")
                    st.exception(error)

if "module2_result" in st.session_state:
    st.markdown("---")
    render_prediction_result(st.session_state["module2_result"])

render_footer()
