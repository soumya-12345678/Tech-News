from flask import Flask, request, jsonify
from news_api_fetcher import fetch_news_api_tech
from news_fetcher import fetch_rss_tech
from summerizer import generate_contextual_summary
import pandas as pd
import spacy

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

@app.route("/")
def home():
    news_api_df = fetch_news_api_tech()
    rss_df = fetch_rss_tech()

    combined_df = pd.concat([news_api_df, rss_df], ignore_index=True)
    combined_df.drop_duplicates(subset="title", inplace=True)
    combined_df = combined_df.sort_values(by="published", ascending=False)

    combined_df["context"] = combined_df.apply(
        lambda row: generate_contextual_summary(row["title"], row["summary"]), axis=1
    )

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI & Software News</title>
        <link rel="stylesheet" href="/static/styles.css">
    </head>
    <body>
    <h2>AI & Software R&D News Portal</h2>
    <p>Stay updated on software launches, AI research, and company tech investments.</p>
    <hr>
    """

    if combined_df.empty:
        html += "<p>No relevant technical news found right now. Please check again later.</p>"
    else:
        html += f"<p><b>Total Technical Articles:</b> {len(combined_df)}</p>"
        html += "<ul>"
        for _, news in combined_df.iterrows():
            html += (
                f"<li><a href='{news['link']}' target='_blank'>{news['title']}</a> "
                f"- <strong>{news['source']}</strong><br>"
                f"<em>{news['context']}</em></li>"
            )
        html += "</ul>"

    html += "</body></html>"
    return html

@app.route("/api/query")
def query_news():
    date = request.args.get("date", "today")
    summarize = request.args.get("summarize", "0") == "1"

    df = pd.concat([fetch_news_api_tech(), fetch_rss_tech()], ignore_index=True)
    df.drop_duplicates(subset="title", inplace=True)


    return jsonify({"items": df.to_dict(orient="records")})

@app.route("/refresh")
def refresh():
    df = pd.concat([fetch_news_api_tech(), fetch_rss_tech()], ignore_index=True)
    return jsonify({"count": len(df)})

if __name__ == "__main__":
    app.run(debug=True)
