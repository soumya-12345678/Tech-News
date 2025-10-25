# AI-Based Real-Time Technical News Chatbot (Student Version)

## Overview
This project is a simple, mobile-friendly chatbot that returns **technical news by date** (from Times of India Tech & Hindustan Times Tech RSS feeds). It filters for technical topics, optionally summarizes articles using a Hugging Face summarization model, and displays results in a chat-bubble interface suitable for both phone and laptop browsers.

## Contents
- `app.py` — Flask backend (API + static file serving)
- `news_fetcher.py` — Fetches RSS feeds and filters technical news
- `summarizer.py` — Optional summarizer using Hugging Face pipeline
- `static/` — Frontend files (index.html, styles.css, script.js)
- `news_data.csv` — Example dataset created by the fetcher
- `requirements.txt` — Python dependencies

## Quick setup (Laptop)
1. Install Python 3.8+.
2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate        # macOS/Linux
   venv\Scripts\activate         # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   > Note: `transformers` + `torch` may take time to install and require disk space.
4. Run the app:
   ```bash
   python app.py
   ```
5. Open your browser and go to `http://127.0.0.1:5000` on your laptop.
   - To view on your **phone** when both devices are on the same network:
     1. Find your laptop's local IP (e.g., `192.168.1.10`).
     2. Run the app with host `0.0.0.0`:
        ```bash
        python app.py --host=0.0.0.0
        ```
     3. On your phone's browser go to `http://<laptop-ip>:5000` (e.g., `http://192.168.1.10:5000`).

## Usage
- In the chat box, type natural dates such as: `today`, `yesterday`, `5 Oct 2025`, `2025-10-07`.
- The bot returns a short summary (if summarizer enabled), link, and published time.
- Click **Refresh News** in the UI to fetch the latest RSS articles.

## Notes
- This is a student MVP. Respect each source's Terms of Use. For production or public deployment, consider using licensed news APIs.
- If you do not want summarization (to speed installation), remove `transformers` and `torch` from `requirements.txt` and delete or disable summarizer usage in `app.py`.

