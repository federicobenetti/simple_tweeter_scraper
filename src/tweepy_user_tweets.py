#!/usr/bin/env python3
"""
tweepy_user_tweets.py (legacy, deprecated)

- Reads secrets from env or .env
- Simple CLI
- Keeps v1.1 Tweepy logic (may break due to X changes)

Usage:
  python src/tweepy_user_tweets.py --users nytimes,BBCNews --start-date 2022-01-01 --ndays 7 --output data/tweets.csv
Env:
  TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
"""
import argparse, os, time, random
from datetime import datetime, timedelta
import pandas as pd
from dotenv import load_dotenv
from dateutil import parser as dtparser
import tweepy

def get_api():
    load_dotenv()
    k = os.getenv("TWITTER_API_KEY")
    s = os.getenv("TWITTER_API_SECRET")
    t = os.getenv("TWITTER_ACCESS_TOKEN")
    ts = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    if not all([k,s,t,ts]):
        raise RuntimeError("Missing Twitter credentials in environment variables.")
    try:
        auth = tweepy.OAuth1UserHandler(k, s, t, ts)
    except AttributeError:
        auth = tweepy.OAuthHandler(k, s); auth.set_access_token(t, ts)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api

def get_user_tweets(api, user, start_date, ndays):
    end_date = start_date + timedelta(days=ndays)
    tweets = api.user_timeline(screen_name=user, count=200, include_rts=False, tweet_mode="extended")
    all_tweets = list(tweets) if tweets else []
    while all_tweets:
        last = all_tweets[-1]
        last_dt = getattr(last, "created_at", None)
        last_dt = last_dt.replace(tzinfo=None) if last_dt is not None else None
        if last_dt and last_dt.date() + timedelta(days=1) <= start_date.date():
            break
        more = api.user_timeline(screen_name=user, count=150, include_rts=False, max_id=last.id-1, tweet_mode="extended")
        if not more: break
        all_tweets.extend(more)
        time.sleep(random.uniform(0.5, 1.25))
    rows = [[
        getattr(t, "id_str", ""),
        getattr(t, "created_at", None).replace(tzinfo=None) if getattr(t, "created_at", None) else None,
        getattr(t, "favorite_count", None),
        getattr(t, "retweet_count", None),
        getattr(t, "full_text", ""),
        user
    ] for t in all_tweets]
    df = pd.DataFrame(rows, columns=["id","created_at","favorite_count","retweet_count","text","username"])
    df = df.dropna(subset=["created_at"])
    df = df[(df["created_at"] >= start_date) & (df["created_at"] <= end_date)]
    return df

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--users", required=True)
    ap.add_argument("--start-date", default="2022-01-01")
    ap.add_argument("--ndays", type=int, default=7)
    ap.add_argument("--output", default="data/tweets.csv")
    args = ap.parse_args()
    start_date = datetime.fromisoformat(args.start_date)
    api = get_api()
    frames = []
    for u in [x.strip() for x in args.users.split(",") if x.strip()]:
        try:
            print(f"Scraping @{u} ...")
            frames.append(get_user_tweets(api, u, start_date, args.ndays))
        except Exception as e:
            print(f"Warning: {u}: {e}")
    if frames:
        out = pd.concat(frames, ignore_index=True)
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        out.to_csv(args.output, index=False)
        print(f"Saved {len(out):,} rows to {args.output}")
    else:
        print("No data collected.")
if __name__ == "__main__":
    main()
