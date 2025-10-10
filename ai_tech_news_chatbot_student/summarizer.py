# Lightweight summarizer without transformers
def summarize_text(text, max_length=300):
    """
    Simple summarizer: truncate text to max_length characters.
    """
    text = str(text)
    if len(text) <= max_length:
        return text
    else:
        return text[:max_length] + "..."
