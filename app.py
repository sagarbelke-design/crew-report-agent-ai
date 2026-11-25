import re

import streamlit as st

from crew import build_report_crew


def make_download_filename(topic: str) -> str:
    """Create a safe Markdown filename beginning with the topic."""
    prefix = re.sub(r"[^A-Za-z0-9]+", "-", topic.strip()).strip("-").lower()
    return f"{prefix or 'report'}-report.md"


st.set_page_config(page_title="CrewAI Report Generator", layout="wide")
st.title("Multi-Agent Markdown Report Generator")
st.caption("Powered by CrewAI, Ollama, and Streamlit")

topic = st.text_input("Report topic", placeholder="Enter a topic...")

if st.button("Generate Report", type="primary"):
    if not topic.strip():
        st.warning("Please enter a topic before generating the report.")
        st.stop()

    try:
        report_crew = build_report_crew()
        with st.spinner("The research, writing, and review agents are working..."):
            result = report_crew.kickoff(inputs={"topic": topic.strip()})

        final_report = str(result)
        st.markdown(final_report)
        st.download_button(
            label="Download Markdown",
            data=final_report,
            file_name=make_download_filename(topic),
            mime="text/markdown",
        )
    except Exception as error:
        error_message = str(error)
        st.error(f"Report generation failed: {error_message}")

        if "connection" in error_message.lower() or "refused" in error_message.lower():
            st.info(
                "Please check that Ollama is running locally and that the "
                "configured model is available."
            )
