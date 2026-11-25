from crewai import Task

from agents import researcher, reviewer, writer


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
    expected_output="A complete Markdown report, with headings and a source list.",
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
