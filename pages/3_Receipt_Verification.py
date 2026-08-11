import streamlit as st

from app import (
    apply_theme,
    page_header,
    render_footer,
    render_prediction_result,
    render_sidebar,
    save_uploaded_file,
)

from inference.receipt_detector import verify_receipt


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Receipt Verification | VeriShield AI",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# GLOBAL UI
# ============================================================

apply_theme()
render_sidebar()

page_header(
    "Receipt Verification",
    (
        "Extract OCR text, verify receipt fields, validate metadata, "
        "and calculate receipt integrity score."
    ),
)


# ============================================================
# MODULE INFORMATION
# ============================================================

st.info(
    "Module 2 uses EasyOCR and rule-based metadata validation. "
    "It does not use Grad-CAM, heatmap, or a trained image classifier."
)


# ============================================================
# FILE UPLOAD
# ============================================================

uploaded_file = st.file_uploader(
    "Upload receipt image",
    type=["jpg", "jpeg", "png", "bmp", "webp"],
    key="module2_uploader",
)


# ============================================================
# RECEIPT PROCESSING
# ============================================================

if uploaded_file is not None:

    # Save only when a genuinely different file is uploaded.
    # This prevents duplicate files during Streamlit reruns.
    if (
        st.session_state.get("module2_uploaded_name")
        != uploaded_file.name
    ):
        st.session_state["module2_image_path"] = (
            save_uploaded_file(uploaded_file)
        )

        st.session_state["module2_uploaded_name"] = (
            uploaded_file.name
        )

        # New upload = previous result is no longer valid.
        st.session_state.pop("module2_result", None)

    image_path = st.session_state.get("module2_image_path")

    if image_path:

        left, right = st.columns(
            [0.9, 1.1],
            gap="large",
        )

        # ====================================================
        # LEFT: UPLOADED RECEIPT
        # ====================================================

        with left:

            st.markdown("### Uploaded Receipt")

            st.image(
                str(image_path),
                width="stretch",
            )

        # ====================================================
        # RIGHT: VERIFICATION
        # ====================================================

        with right:

            st.markdown("### Verification")

            st.markdown(
                """
                <div class="soft-card">
                    <p>
                        The system will run OCR, extract merchant and invoice
                        fields, validate date and amount consistency,
                        calculate the receipt integrity score, and generate
                        JSON/PDF reports.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.write("")

            if st.button(
                "Verify Receipt",
                width="stretch",
                type="primary",
            ):

                with st.spinner(
                    "Loading OCR engine and verifying receipt..."
                ):

                    try:

                        result = verify_receipt(image_path)

                        st.session_state["module2_result"] = result

                    except Exception as error:

                        st.session_state.pop(
                            "module2_result",
                            None,
                        )

                        st.error(
                            "Receipt verification failed."
                        )

                        st.exception(error)


# ============================================================
# DISPLAY RESULT
# ============================================================

if "module2_result" in st.session_state:

    st.markdown("---")

    render_prediction_result(
        st.session_state["module2_result"]
    )


# ============================================================
# FOOTER
# ============================================================

render_footer()