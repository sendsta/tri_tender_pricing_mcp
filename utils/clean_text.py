import re


def clean_text(text: str) -> str:
    """Basic normalisation for tender documents."""
    if not text:
        return ""

    # Normalise whitespace
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    # Collapse many blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()
