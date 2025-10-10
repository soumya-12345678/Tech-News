import argparse
from flask import Flask, jsonify, request, send_from_directory, render_template
from flask import send_file
import pandas as pd
from datetime import datetime
import dateparser
from news_fetcher import fetch_technical_news
from summarizer import summarize_text
import os

app = Flask(__name__, static_folder="static", template_folder="static")

DATA_FILE = "news_data.csv"

@app.route("/")
def index():
    return send_file("static/index.html")

@app.route("/refresh")
def refresh():
    df = fetch_technical_news()
    return jsonify({"status":"ok", "count": len(df)})

def load_data():
    if not os.path.exists(DATA_FILE):
        # create by fetching once
        fetch_technical_news()
    try:
        df = pd.read_csv(DATA_FILE)
    except Exception:
        df = pd.DataFrame(columns=["title","summary","link","published","source"])
    return df

@app.route("/api/query")
def api_query():
    """
    Query params:
      q  - optional text (not used heavily now)
      date - natural language date e.g. 'today', '5 Oct 2025', 'yesterday'
      summarize - '1' or '0' default '1'
    """
    q = request.args.get("q", "")
    date_str = request.args.get("date", "today")
    summarize_flag = request.args.get("summarize", "1")
    date_obj = dateparser.parse(date_str)
    if not date_obj:
        return jsonify({"error":"could not parse date"}), 400
    selected_date = date_obj.date()
    df = load_data()
    if df.empty:
        return jsonify({"items":[]})
    df['date'] = pd.to_datetime(df['published'], errors='coerce').dt.date
    filtered = df[df['date'] == selected_date]
    items = []
    for _, row in filtered.iterrows():
        txt = row.get("summary", "") or row.get("title","")
        summary = txt
        if summarize_flag == "1":
            try:
                summary = summarize_text(str(txt))
            except Exception:
                summary = txt if len(txt) < 300 else txt[:300] + "..."
        items.append({
            "title": row.get("title"),
            "summary": summary,
            "link": row.get("link"),
            "published": row.get("published"),
            "source": row.get("source")
        })
    return jsonify({"items": items})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=True)
