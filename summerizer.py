import spacy

nlp = spacy.load("en_core_web_sm")

def generate_contextual_summary(title, description):
    text = f"{title}. {description}"
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents]
    if len(sentences) >= 2:
        return " ".join(sentences[:2])
    return text.strip()
