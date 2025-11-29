from pathlib import Path
from typing import Union

import pdfplumber


def read_pdf_text(path: Union[str, Path]) -> str:
    """Read and concatenate text from a PDF file using pdfplumber."""
    p = Path(path)
    if not p.exists():
        return ""

    texts = []
    try:
        with pdfplumber.open(str(p)) as pdf:
            for page in pdf.pages:
                try:
                    txt = page.extract_text() or ""
                    texts.append(txt)
                except Exception:
                    continue
    except Exception:
        return ""

    return "\n".join(texts)
