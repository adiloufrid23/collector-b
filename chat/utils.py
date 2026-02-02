import re

EMAIL_RE = re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", re.I)
PHONE_RE = re.compile(r"\b(\+?\d[\d\s\-\(\)]{7,}\d)\b")

def contains_personal_info(text: str) -> bool:
    return bool(EMAIL_RE.search(text) or PHONE_RE.search(text))
