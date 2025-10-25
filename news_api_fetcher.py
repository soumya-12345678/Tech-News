import requests
import pandas as pd
from datetime import datetime
import spacy
import re
from bs4 import BeautifulSoup

nlp = spacy.load("en_core_web_sm")

NEWS_API_KEY = "7f2a7b9c915d4a8eb8f33bb8a184e417"

TECH_TERMS = [
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
    "Morgan Stanley","IBM","Cognizant","Accenture","Capgemini","DXC Technology","HCL Technologies","LTI","Tech Mahindra"
]


def clean_summary(text):
    return BeautifulSoup(text, "html.parser").get_text()

def is_relevant(text):
    keyword_match = any(term.lower() in text for term in TECH_TERMS + COMPANY_TERMS)
    phrase_match = bool(re.search(r"(raised|secured|funding|launched|announced).*?(million|platform|product|model)", text))
    doc = nlp(text)
    orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    money = [ent.text for ent in doc.ents if ent.label_ == "MONEY"]
    entity_boost = bool(orgs or money)
    return keyword_match or phrase_match or entity_boost

def fetch_news_api_tech():
    url = (
        "https://newsapi.org/v2/everything?"
        "q=(AI OR software OR cloud OR R&D OR investment OR developer OR startup)"
        "&language=en&sortBy=publishedAt&pageSize=30&apiKey=" + NEWS_API_KEY
    )

    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        print("Error fetching from NewsAPI:", e)
        return pd.DataFrame()

    articles = data.get("articles", [])
    all_news = []

    for a in articles:
        title = a.get("title", "")
        desc = clean_summary(a.get("description", ""))
        text = (title + " " + desc).lower()

        if is_relevant(text):
            all_news.append({
                "title": title,
                "summary": desc,
                "link": a.get("url"),
                "published": a.get("publishedAt", datetime.utcnow().isoformat()),
                "source": a.get("source", {}).get("name", "")
            })

    df = pd.DataFrame(all_news)
    if not df.empty:
        df['published'] = pd.to_datetime(df['published'], errors='coerce').astype(str)
    return df
