import requests
import pandas as pd
from datetime import datetime

NEWS_API_KEY = "7f2a7b9c915d4a8eb8f33bb8a184e417"

def fetch_news_api_tech():
    url = (
        f"https://newsapi.org/v2/top-headlines?"
        f"category=technology&language=en&apiKey={NEWS_API_KEY}"
    )

    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        print("Error fetching news from NewsAPI:", e)
        return pd.DataFrame()

    articles = data.get("articles", [])
    all_news = []

    for a in articles:
        all_news.append({
            "title": a.get("title"),
            "summary": a.get("description", ""),
            "link": a.get("url"),
            "published": a.get("publishedAt", datetime.utcnow().isoformat()),
            "source": a.get("source", {}).get("name", "")
        })

    df = pd.DataFrame(all_news)
    if not df.empty:
        df['published'] = pd.to_datetime(df['published'], errors='coerce').fillna(pd.Timestamp.utcnow()).astype(str)
    df.to_csv("news_data.csv", index=False)
    return df
