import feedparser
import pandas as pd
from datetime import datetime
from typing import List
from dateparser import parse as dateparse

# RSS feeds focused on Tech sections
RSS_FEEDS = [
    "https://timesofindia.indiatimes.com/rssfeeds/66949542.cms",  # TOI Tech (may change)
    "https://www.hindustantimes.com/feeds/rss/tech/rssfeed.xml"   # HT Tech
]

TECH_KEYWORDS = [
    "technology", "ai", "artificial intelligence", "machine learning",
    "software", "hardware", "gadgets", "robotics", "electronics",
    "innovation", "startup", "engineering", "research", "science", "telecom", "cloud"
]

def is_technical(title: str, summary: str) -> bool:
    txt = (title + " " + summary).lower()
    return any(k.lower() in txt for k in TECH_KEYWORDS)

def fetch_technical_news() -> pd.DataFrame:
    all_news = []
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
        except Exception as e:
            print("Failed to parse", url, e)
            continue
        for entry in feed.entries:
            title = entry.get("title", "")
            summary = entry.get("summary", "")
            link = entry.get("link", "")
            published = entry.get("published", entry.get("pubDate", datetime.utcnow().isoformat()))
            if is_technical(title, summary):
                all_news.append({
                    "title": title,
                    "summary": summary,
                    "link": link,
                    "published": published,
                    "source": url
                })
    df = pd.DataFrame(all_news)
    if not df.empty:
        # normalize published to ISO
        df['published'] = pd.to_datetime(df['published'], errors='coerce').fillna(pd.Timestamp.utcnow()).astype(str)
        df.to_csv("news_data.csv", index=False)
    else:
        # create empty CSV if none
        df.to_csv("news_data.csv", index=False)
    return df

if __name__ == "__main__":
    df = fetch_technical_news()
    print("Fetched", len(df), "technical articles")
