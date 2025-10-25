import feedparser
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

RSS_FEEDS = [
    "https://www.zdnet.com/news/rss.xml",
    "https://www.theverge.com/rss/index.xml",
    "https://timesofindia.indiatimes.com/rssfeeds/66949542.cms",
    "https://www.hindustantimes.com/feeds/rss/tech/rssfeed.xml"
]

SOFTWARE_TERMS = [
    # AI & ML
    "AI research", "AI R&D", "artificial intelligence", "machine learning", "deep learning",
    "AI accelerator", "AI infrastructure", "AI chip", "AI startup", "AI breakthrough",

    # Software & Developer Tools
    "software engineering", "developer tools", "cloud computing", "data science",
    "API platform", "SDK", "framework", "automation tools", "enterprise SaaS",

    # Launches & Innovation
    "product launch", "software release", "platform launch", "innovation lab",
    "new feature", "beta release", "technical preview", "developer conference",

    # Investment & Funding
    "startup funding", "series A", "series B", "tech investment", "R&D investment",
    "venture capital", "strategic partnership", "research grant", "AI funding"
]

COMPANY_TERMS = [
    "OpenAI", "DeepMind", "Anthropic", "NVIDIA", "Microsoft Research",
    "Meta AI", "Amazon Web Services", "Google Cloud", "IBM Watson",
    "Databricks", "Salesforce", "Oracle", "SAP", "Intel", "Qualcomm",
    "Adobe", "Snowflake", "Palantir", "UiPath", "ServiceNow","Infosys",
    "Wipro","Tata Consultancy Services","Goldman Sachs","JPMorgan Chase",
    "Morgan Stanley","IBM","Cognizant","Accenture","Capgemini","DXC Technology",
    "HCL Technologies","LTI","Tech Mahindra","Virtusa","Mphasis","Zensar Technologies"
]

def clean_summary(text):
    return BeautifulSoup(text, "html.parser").get_text()

def fetch_rss_tech():
    all_news = []
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
        except Exception as e:
            print("Failed to parse", url, e)
            continue

        for entry in feed.entries:
            title = entry.get("title", "")
            summary = clean_summary(entry.get("summary", ""))
            link = entry.get("link", "")
            published = entry.get("published", datetime.utcnow().isoformat())
            text = (title + " " + summary).lower()

            if any(k.lower() in text for k in SOFTWARE_TERMS + COMPANY_TERMS):
                all_news.append({
                    "title": title,
                    "summary": summary,
                    "link": link,
                    "published": published,
                    "source": url
                })

    df = pd.DataFrame(all_news)
    if not df.empty:
        df['published'] = pd.to_datetime(df['published'], errors='coerce').astype(str)
    return df
