# startup-data-pipeline

Automated pipeline that discovers recently funded startups, resolves company identity, detects active technical hiring through ATS APIs, ranks opportunities, and publishes results to downstream destinations.

## Project Structure

- `app/extract`: LLM-driven parsing helpers.
- `app/hiring`: Detection of applicant tracking systems and role classification.
- `app/ingest`: RSS and data ingestion workflows.
- `app/publish`: Publishers (Slack alerts, Google Sheets, etc.).
- `app/resolve`: Domain and company resolution utilities.
- `app/store`: Persistence models and SQL schema.
- `data`: Sample payloads and cached artifacts.
- `config`: Configuration templates.
- `tests`: Lightweight unit tests for core modules.
- `main.py`: Entry point wiring together the pipeline steps.

## Getting Started

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```
