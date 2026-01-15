# Ceradon SAM Opportunity Bot

Ceradon SAM Opportunity Bot is a hardened, offline-first Python service that queries the official SAM.gov Get Opportunities Public API, normalizes and scores contract opportunities for Ceradon Systems, deduplicates results locally in SQLite, and sends a daily email digest. It is designed for Raspberry Pi / Debian-class hosts in low-connectivity environments.

## Why this design
- **API-only**: No scraping, strictly uses the official SAM.gov public API.
- **Offline-first**: Local SQLite storage and rotating logs, no cloud dependencies.
- **Deterministic scoring**: Transparent keyword and metadata boosts, no ML.
- **Edge friendly**: Minimal dependencies, predictable runtime behavior.

## Tooling choice
This project is structured for **uv** (fast, offline-friendly dependency management). You can still use pip or Poetry, but uv is recommended for Raspberry Pi deployments.

## Requirements
- Python 3.9+
- A SAM.gov public API key
- Google Workspace / Gmail App Password for SMTP

## Setup

### 1) Obtain a SAM.gov API key
1. Create an account at https://sam.gov
2. Request a public API key in the API key management section.
3. Export the key as an environment variable:
   ```bash
   export SAM_API_KEY="your_key_here"
   ```

### 2) Create a Google App Password
1. Enable 2-Step Verification on your Google account.
2. Create an **App Password** for "Mail".
3. Export the app password:
   ```bash
   export SMTP_PASS="your_app_password"
   ```

### 3) Install dependencies (Raspberry Pi)
Using uv:
```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

Using pip:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 4) Configure
Copy the example config and edit as needed:
```bash
cp config/config.example.yaml config/config.yaml
```

### 5) Run once
```bash
make run-once
```

## CLI usage
```bash
ceradon-sam-bot run --config config/config.yaml --once
ceradon-sam-bot run --config config/config.yaml --daemon --interval-minutes 1440
ceradon-sam-bot backfill --config config/config.yaml --days 60
ceradon-sam-bot export --format csv --since-days 30
ceradon-sam-bot explain --notice-id <id>
```

## Environment variables
Required:
- `SAM_API_KEY`
- `SMTP_PASS`

Optional (defaults shown):
- `SMTP_HOST` (smtp.gmail.com)
- `SMTP_PORT` (587)
- `SMTP_USER` (noah@ceradonsystems.com)
- `EMAIL_TO` (noah@ceradonsystems.com)
- `EMAIL_FROM` (noah@ceradonsystems.com)
- `BOT_DATA_DIR` (/var/lib/ceradon-sam-bot)
- `SAM_API_KEY_IN_QUERY` (false) to use query parameter auth instead of header

## Storage and logs
- SQLite database: `${BOT_DATA_DIR}/ceradon_sam_bot.sqlite`
- Logs: `${BOT_DATA_DIR}/logs/ceradon_sam_bot.log`

## Cron example (daily 06:30)
```cron
30 6 * * * /usr/bin/env SAM_API_KEY=... SMTP_PASS=... BOT_DATA_DIR=/var/lib/ceradon-sam-bot \
  /usr/bin/ceradon-sam-bot run --config /path/to/config.yaml --once >> /var/lib/ceradon-sam-bot/cron.log 2>&1
```

## Tuning filters and scoring safely
- **NAICS filters**: Update `filters.naics_include` to expand or tighten scope.
- **Notice types**: Keep `filters.exclude_notice_types` strict to avoid award notices.
- **Keyword weights**: Favor positive weights for R&D and sensing terms; keep negative weights high for construction and commodity reselling.
- **Threshold**: Increase `scoring.include_in_digest_score` to reduce digest size.

## Docker
```bash
docker compose up --build
```

## Checklist (first run)
- [ ] SAM API key exported (`SAM_API_KEY`)
- [ ] SMTP app password exported (`SMTP_PASS`)
- [ ] `config.yaml` created from example
- [ ] `make run-once` completes successfully
- [ ] Daily cron scheduled
