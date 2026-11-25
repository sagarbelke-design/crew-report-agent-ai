import re

import streamlit as st
from crewai import Agent, Crew, LLM, Process, Task


OLLAMA_MODEL = "qwen3:1.7b"
OLLAMA_BASE_URL = "http://localhost:11434"


# Configure Ollama once for all three agents.
llm = LLM(
    model=f"ollama/{OLLAMA_MODEL}",
    base_url=OLLAMA_BASE_URL,
)


researcher = Agent(
    role="Senior Research Analyst",
    goal="Produce a concise, evidence-based brief for the topic: {topic}",
    backstory=(
        "You are a meticulous researcher who separates facts from opinions "
        "and always cites sources."
    ),
    llm=llm,
    verbose=False,
)


writer = Agent(
    role="Technical Report Writer",
    goal="Transform the research brief into a well-structured Markdown report",
    backstory=(
        "You excel at organizing complex information into clear sections "
        "with logical flow."
    ),
    llm=llm,
    verbose=False,
)


reviewer = Agent(
    role="Quality Reviewer",
    goal="Ensure the report is clear, complete, evidence-based, and free of unsupported claims",
    backstory=(
        "You are a strict editor who checks every claim against the original brief "
        "and flags gaps."
    ),
    llm=llm,
    verbose=False,
)


research_task = Task(
    description=(
        "Research the topic '{topic}'. Gather key facts, statistics, and viewpoints. "
        "Produce an evidence brief with bullet points and source notes."
    ),
    expected_output=(
        "A structured evidence brief in Markdown, with facts and source references."
    ),
    agent=researcher,
)


writer_task = Task(
    description=(
        "Using the research brief, write a complete Markdown report on '{topic}'. "
        "Include Introduction, Main Analysis, and Conclusion. "
        "Every claim must be traceable to the brief."
    ),
    expected_output=(
        "A complete Markdown report, with headings and a source list."
    ),
    agent=writer,
    context=[research_task],
)


reviewer_task = Task(
    description=(
        "Review the report against the original research brief. Check for: "
        "clarity, completeness, evidence usage, and unsupported claims. "
        "Return the refined final Markdown report with corrections applied."
    ),
    expected_output=(
        "The final reviewed and refined Markdown report, ready for display/download."
    ),
    agent=reviewer,
    context=[research_task, writer_task],
)


report_crew = Crew(
    agents=[researcher, writer, reviewer],
    tasks=[research_task, writer_task, reviewer_task],
    process=Process.sequential,
    verbose=False,
)


def make_download_filename(topic: str) -> str:
    """Create a safe Markdown download filename beginning with the topic."""
    prefix = re.sub(r"[^A-Za-z0-9]+", "-", topic.strip()).strip("-").lower()
    return f"{prefix or 'report'}-report.md"


st.set_page_config(page_title="CrewAI Report Generator", layout="wide")
st.title("Multi-Agent Markdown Report Generator")
st.caption("Powered by CrewAI, Ollama (qwen3:1.7b), and Streamlit")

topic = st.text_input("Report topic", placeholder="Enter a topic...")

if st.button("Generate Report", type="primary"):
    if not topic.strip():
        st.warning("Please enter a topic before generating the report.")
        st.stop()

    try:
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
                "Please check that Ollama is running locally and that "
                "qwen3:1.7b is available (try: ollama pull qwen3:1.7b)."
            )
