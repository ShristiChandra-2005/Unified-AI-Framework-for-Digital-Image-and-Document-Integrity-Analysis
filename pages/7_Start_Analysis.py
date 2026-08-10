import streamlit as st

from app import (
    apply_theme,
    page_header,
    render_footer,
    render_sidebar,
    render_start_analysis,
)

st.set_page_config(
    page_title="Start Analysis | VeriShield AI",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
render_sidebar()

page_header(
    "Start Analysis",
    "Select one analysis module and begin image or document integrity verification.",
)

render_start_analysis()

render_footer()
