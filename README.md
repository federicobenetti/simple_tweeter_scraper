# simple_tweeter_scraper 🐦 (deprecated)

> **Status: Deprecated** — Twitter became **X** and legacy credentials/endpoints may no longer work.  
> This repository is preserved for reference and educational use. Consider alternatives like **snscrape** or the official **X API v2**.

Minimal pipeline to **collect user tweets** (legacy Tweepy v1.1) and **clean/analyze** them via a small CLI.

## 📦 What’s inside
- `src/tweepy_user_tweets.py` — legacy scraper (reads secrets from env or `.env`).
- `src/clean_tweets.py` — cleaner & quick metrics (CSV in, CSVs out).
- `requirements.txt`, `.gitignore` (with deprecation note), `.env.example`, `LICENSE`.

## 🚀 Quickstart
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # fill secrets if you still have working access
```

### Scrape (may fail on X now)
```bash
python src/tweepy_user_tweets.py --users nytimes,BBCNews --start-date 2022-01-01 --ndays 7 --output data/tweets.csv
```

### Clean / analyze
```bash
python src/clean_tweets.py --input data/tweets.csv --out-prefix results/tweets
```

## 🔐 Secrets
Set these as environment variables (or in a local `.env`, not committed):
- `TWITTER_API_KEY`, `TWITTER_API_SECRET`
- `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_TOKEN_SECRET`

