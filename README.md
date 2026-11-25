# CrewAI + Ollama Multi-Agent Report Generator

A Streamlit application that uses three sequential CrewAI agents with the local
Ollama `qwen3:1.7b` model to research a topic and generate a reviewed Markdown
report. The project separates UI, configuration, agents, tasks, and crew setup.

## Prerequisites

- Python 3.10 or newer
- Ollama installed and running

## Setup

1. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Download the Ollama model:

   ```powershell
   ollama pull qwen3:1.7b
   ```

4. Start the Streamlit application:

   ```powershell
   streamlit run app.py
   ```

The application uses Ollama at `http://localhost:11434`. Enter a topic in the
browser UI, generate the report, and download the final Markdown result.

## Project Structure

- `app.py` - Streamlit interface and error handling
- `config.py` - Ollama model and server configuration
- `agents.py` - Researcher, Writer, and Reviewer agents
- `tasks.py` - Dedicated tasks and context chaining
- `crew.py` - Sequential CrewAI crew construction
- `requirements.txt` - Python dependencies
