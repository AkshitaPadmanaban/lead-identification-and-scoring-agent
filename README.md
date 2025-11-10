# Startup Funding & Hiring Signal Pipeline

Automated system that discovers venture funding rounds, enriches each company with hiring intelligence, persists results for deduped history, and publishes fresh leads to Google Sheets for immediate outreach. Built as the technical assignment for **CodeRound AI**.

## Highlights

- **Funding discovery:** Pulls high-signal press releases for the last _n_ days (default 7, configurable up to 30+) and normalises amounts, rounds, investors, and announcement dates via Gemini 2.5 Flash.
- **Company enrichment:** Resolves official domains directly from the press article (before search/guessing) to avoid false positives, then captures source URLs for traceability.
- **Hiring detection:** Identifies ATS links (Greenhouse, Lever, Ashby, Workable, BambooHR, etc.), scrapes role metadata, and grades companies into tiers (A recent tech hiring, B tech roles but older, C no active tech hiring).
- **Persistence & dedupe:** Stores snapshots in `data/companies.db` (SQLite) with a uniqueness constraint on `(company_name, funding_round, announcement_date)` so re-runs update the latest data instead of duplicating rows.
- **Go-to-market output:** Publishes every run to a Google Sheet (`Recently Funded Startups`) so sales/BD can act without touching the database.
- **Extensible foundation:** Clean module boundaries (`app/ingest`, `app/extract`, `app/resolve`, `app/hiring`, `app/store`, `app/publish`) make it easy to add LinkedIn enrichment, Slack notifications, or Docker packaging later.

## System Flow

1. **Fetch** funding news via curated RSS feeds.
2. **Parse** each article with Gemini to extract structured JSON.
3. **Resolve** domains using hyperlinks in the press release (fallback to DuckDuckGo + smart guessing).
4. **Detect hiring** by scanning ATS boards or `/careers` pages for tech titles posted in the last 14 days.
5. **Persist** into SQLite (dedupe on company/round/date) and append to Google Sheets.
6. (Optional) Use the stored data to drive alerts/analytics.

## Setup

### Requirements

- Python 3.10+
- Google service account with Sheets API enabled
- Gemini API key (Google AI Studio)

### 1. Clone & install dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure secrets

1. **Gemini**: create an `.env` file in the repo root:
   ```env
   GEMINI_API_KEY=your-google-gemini-key
   ```
   _(Optional) If you plan to use the OpenAI test helper, add `OPENAI_API_KEY=...` as well._

2. **Google Sheets credentials**:
   - Download your service-account JSON and save it as `gen-lang-client-0811071215-3e0f9f2c4083.json` in the repo root (match the filename or adjust `app/publish/to_gsheet.py`).
   - Share the target Sheet (`Recently Funded Startups`) with the service-account email.

### 3. (Optional) Sanity check API keys

```bash
python scripts/test_openai_key.py   # requires OPENAI_API_KEY
```

## Running the Pipeline

```bash
python main.py
```

What happens:

- Logs progress for each step (fetch → enrich → resolve → hiring → DB → Sheets).
- Writes/updates `data/companies.db` with deduped company rows.
- Appends the latest run to the Google Sheet so go-to-market teams can work off it immediately.

### Inspecting results

```bash
# Show total stored rows
sqlite3 data/companies.db 'SELECT COUNT(*) FROM funded_companies;'

# Peek at the most recent companies
sqlite3 data/companies.db "SELECT company_name, amount_raised_usd, hiring_tier, last_seen FROM funded_companies ORDER BY last_seen DESC LIMIT 10;"
```

## Configuration & Tuning

- **`days_back` / max leads**: adjust `fetch_recent_articles(days_back=7)[:20]` in `main.py` to widen the time window or increase throughput.
- **Hiring recency window**: tweak `RECENT_DAYS` in `app/hiring/detect_ats.py` (defaults to 14 days).
- **Supported ATS providers**: see `ATS_PATTERNS` inside `detect_ats.py` to add/remove vendors.
- **Prompt controls**: the enrichment prompt lives in `app/extract/llm_parse.py`; guardrails ensure Gemini returns clean JSON even when articles are noisy.

## Rate Limits & Cost Considerations

- **Gemini 2.5 Flash**: lightweight but still billed per token—limiting to 20 articles per run keeps cost low. Increase gradually and monitor usage in Google AI Studio.
- **Hiring detectors**: Uses public ATS APIs or HTML scraping; we include polite timeouts and minimal concurrency to avoid hammering vendor sites.
- **Google Sheets**: `append_rows` batches updates to stay within quota.

## Roadmap / Future Enhancements

- Slack or email alerts when a company transitions into Hiring Tier A/B.
- LinkedIn + key decision maker enrichment (Clearbit, People Data Labs, etc.).
- Docker/`docker-compose` packaging for one-command deployment (web + scheduler).
- Additional data sources (Crunchbase/Tracxn API) when licence keys are available.
- UI/dashboard to visualise funding + hiring trends.

## Submission Checklist for CodeRound AI

- ✅ GitHub repo with full source, history, and instructions.
- ✅ README covering setup, design decisions, rate-limit considerations, and next steps.
- ✅ Google Sheet showing real output ready for sales outreach.
- ⏳ Add screen-recorded demo walking through the pipeline (per assignment instructions).

Feel free to reach out if you need help adjusting the footprint, adding alerting, or preparing the demo.
