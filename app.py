import tempfile
from pathlib import Path

import streamlit as st

from insight import run_pipeline

st.set_page_config(page_title="InsightPress")
st.title("InsightPress")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
progress_bar = st.progress(0)
status_placeholder = st.empty()

if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = None

def generate_report(file):
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = Path(tmpdir) / "input.csv"
        csv_path.write_bytes(file.getvalue())

        def callback(stage: str, index: int, total: int) -> None:
            progress_bar.progress(int((index / total) * 100))
            status_placeholder.write(f"Stage: {stage}")

        pdf_path = run_pipeline(csv_path, Path(tmpdir), progress_callback=callback)
        st.session_state.pdf_bytes = pdf_path.read_bytes()
        progress_bar.progress(100)
        status_placeholder.write("Done")

if uploaded_file is not None and st.button("Generate InsightPress Report"):
    generate_report(uploaded_file)

if st.session_state.pdf_bytes is not None:
    st.download_button(
        label="Download PDF",
        data=st.session_state.pdf_bytes,
        file_name="report.pdf",
        mime="application/pdf",
    )
