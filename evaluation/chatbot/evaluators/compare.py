import re
from difflib import SequenceMatcher


def normalize_text(text: str) -> str:
def normalize_text(text: str) -> str:
    # 1 lowercase
    text = text.lower()
    # 2 remove special characters
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    # 3 remove extra spaces
    text = re.sub(r"\s+", " ", text)
    # 4 remove accents/diacritics (normalize unicode)
    # text = unicodedata.normalize('NFKD', text)
    # text = "".join(c for c in text if not unicodedata.combining(c))
    # 5 remove leading and trailing spaces
    text = text.strip()
    # 6 remove new lines
    text = re.sub(r"\n+", " ", text)
    # 7 remove tabs
    text = re.sub(r"\t+", " ", text)
    # 8 remove all whitespace
    text = re.sub(r"\s+", " ", text)
    # 9 Remove punctuation
    text = re.sub(r"[^\w\s]", "", text)
    return text


def is_similar(t1: str, t2: str, threshold: float = 0.95) -> bool:
    return (
        SequenceMatcher(None, normalize_text(t1), normalize_text(t2)).ratio()
        >= threshold
    )
