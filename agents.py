from crewai import Agent, LLM

from config import OLLAMA_BASE_URL, OLLAMA_MODEL


# One Ollama model is shared across the three agents.
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
