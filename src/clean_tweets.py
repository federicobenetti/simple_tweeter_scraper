#!/usr/bin/env python3
"""
clean_tweets.py

- CLI for cleaning tweets CSV and producing simple metrics and word frequencies
Usage:
  python src/clean_tweets.py --input data/tweets.csv --out-prefix results/tweets
Outputs:
  results/tweets_clean.csv
  results/tweets_top.csv
  results/tweets_wordfreq.csv
"""
import argparse, os, re, pandas as pd

def extract_first_url(text: str) -> str:
    m = re.search(r'https?://\S+', text or '')
    return m.group(0) if m else ''

def remove_urls(text: str) -> str:
    return re.sub(r'https?://\S+', '', text or '').strip()

def build_wordfreq(df: pd.DataFrame) -> pd.DataFrame:
    try:
        import nltk; from nltk.corpus import stopwords
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords', quiet=True)
        stops = set(stopwords.words('english'))
    except Exception:
        stops = set()
    tokens = []
    for _, r in df.iterrows():
        toks = re.findall(r"[A-Za-z0-9']+", str(r.get('text','')).lower())
        tokens.extend([t for t in toks if t not in stops and len(t)>1])
    freq = {}
    for t in tokens: freq[t]=freq.get(t,0)+1
    return pd.DataFrame(sorted(freq.items(), key=lambda x: x[1], reverse=True), columns=["word","frequency"])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out-prefix", default="results/tweets")
    args = ap.parse_args()

    df = pd.read_csv(args.input)
    # Normalize
    if 'created_at' in df.columns:
        # leave as-is; can be parsed downstream if needed
        pass
    df['text'] = df['text'].astype(str).str.replace('\n',' ', regex=False)

    # URLs and lengths
    df['first_url'] = df['text'].apply(extract_first_url)
    df['text_nourl'] = df['text'].apply(remove_urls)
    df['nwords'] = df['text_nourl'].apply(lambda x: len(str(x).split()))
    df['nchars'] = df['text_nourl'].str.len()

    # Top liked/RT per user
    liked = df.sort_values('favorite_count', ascending=False).groupby('username', as_index=False).first()
    rt = df.sort_values('retweet_count', ascending=False).groupby('username', as_index=False).first()
    top = liked[['username','id','favorite_count','text','first_url']].merge(
        rt[['username','id','retweet_count','text','first_url']].rename(columns={'first_url':'rt_url'}),
        on='username', suffixes=('_liked','_rt')
    )

    # Word frequencies (overall)
    wf = build_wordfreq(df)

    # Save
    os.makedirs(os.path.dirname(args.out_prefix), exist_ok=True)
    df.to_csv(f"{args.out_prefix}_clean.csv", index=False)
    top.to_csv(f"{args.out_prefix}_top.csv", index=False)
    wf.to_csv(f"{args.out_prefix}_wordfreq.csv", index=False)
    print(f"Saved: {args.out_prefix}_clean.csv, _top.csv, _wordfreq.csv")

if __name__ == "__main__":
    main()
