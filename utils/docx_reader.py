from pathlib import Path
from typing import Union

import docx  # python-docx


def read_docx_text(path: Union[str, Path]) -> str:
    """Read text from a DOCX file."""
    p = Path(path)
    if not p.exists():
        return ""

    try:
        document = docx.Document(str(p))
    except Exception:
        return ""

    parts = []
    for para in document.paragraphs:
        txt = para.text.strip()
        if txt:
            parts.append(txt)
    return "\n".join(parts)
