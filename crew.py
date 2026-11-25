from crewai import Crew, Process

from agents import researcher, reviewer, writer
from tasks import research_task, reviewer_task, writer_task


def build_report_crew() -> Crew:
    """Build the sequential report-generation crew."""
    return Crew(
        agents=[researcher, writer, reviewer],
        tasks=[research_task, writer_task, reviewer_task],
        process=Process.sequential,
        verbose=False,
    )
