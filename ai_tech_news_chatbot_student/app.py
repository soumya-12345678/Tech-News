from flask import Flask
from news_api_fetcher import fetch_news_api_tech
from news_fetcher import fetch_rss_tech
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    # Fetch NewsAPI and RSS news
    news_api_df = fetch_news_api_tech()
    rss_df = fetch_rss_tech()

    # Combine both DataFrames using pd.concat
    combined_df = pd.concat([news_api_df, rss_df], ignore_index=True)

    # Convert to HTML list
    html = "<h2>AI Technical News Chatbot</h2>"
    html += f"<p>Total articles: {len(combined_df)}</p>"
    html += "<ul>"
    for _, news in combined_df.iterrows():
        html += (
            f"<li>"
            f"<a href='{news['link']}' target='_blank'>{news['title']}</a> "
            f"- <strong>{news['source']}</strong> "
            f"({news['published'][:10]})"
            f"</li>"
        )
    html += "</ul>"

    return html

@app.route("/news_api")
def news_api():
    df = fetch_news_api_tech()
    return df.to_json(orient="records")

@app.route("/news_rss")
def news_rss():
    df = fetch_rss_tech()
    return df.to_json(orient="records")

if __name__ == "__main__":
    app.run(debug=True)
