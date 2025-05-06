# Modular LLM Orchestration and Feedback Pipeline

## Purpose
This project implements a modular, local-first LLM orchestration system designed for traceable, auditable, and extensible qualitative research workflows. It provides:
- Task-based LLM routing and prompt versioning
- Comprehensive logging of all interactions
- Human-in-the-loop feedback and review tools
- UI dashboards for log inspection and feedback triage

The goal is to build confidence and control into how AI-driven interviews are reviewed, audited, and improved over time.

Inspired by workflows discussed with Listen Labs, this prototype is built to help scale qualitative research feedback with full traceability and improvement loops.

---

## Key Components

### Orchestration & Task Dispatch
- **main.py**: Entry point for running LLM tasks and logging results
- **router.py**: Task router, model selection, and prompt rendering
- **config.py**: Model and task configuration
- **prompts.py**: Prompt templates with versioning and dynamic filling

### Logging & Metadata
- **logger.py**: Logs all LLM interactions with metadata, prompt version, and errors
- **llm_interactions.jsonl**: Append-only log of all LLM requests and responses

### Feedback & Review
- **feedback_queue.jsonl**: Stores flagged log entries with reason and optional human comment
- **streamlit_app.py**: Dashboard for viewing and filtering LLM logs, and submitting feedback
- **review_feedback_app.py**: Dashboard for reviewing, editing, and exporting feedback entries
- **validate_feedback.py**: Script to validate structure of feedback entries for completeness

---

## Project Structure
```text
.
├── main.py
├── router.py
├── config.py
├── prompts.py
├── logger.py
├── llm_interactions.jsonl
├── feedback_queue.jsonl
├── streamlit_app.py
├── review_feedback_app.py
├── validate_feedback.py
├── requirements.txt
└── README.md
```

---

## Setup & Usage

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your OpenAI API key** in a `.env` file:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

3. **Run orchestration pipeline**
   ```bash
   python main.py
   ```
   This will log all LLM interactions to `llm_interactions.jsonl`.

4. **Review logs and submit feedback**
   ```bash
   streamlit run streamlit_app.py
   ```
   - Filter and inspect logs
   - Mark entries as needing improvement (adds to `feedback_queue.jsonl`)

5. **Review and triage feedback**
   ```bash
   streamlit run review_feedback_app.py
   ```
   - Filter, edit, and mark feedback as reviewed
   - Export filtered feedback to CSV
   - Edits are saved to `reviewed_feedback.jsonl`

6. **Validate feedback structure**
   ```bash
   python validate_feedback.py
   ```
   - Ensures all feedback entries have required fields

---

## Notes
- This project is intended for local use only. No deployment or cloud integration is configured.
- Designed for extensibility: add new tasks, prompt templates, or review workflows as needed.
- Built as a prototype for Listen Labs and similar research teams to scale qualitative feedback with traceability and improvement loops. 