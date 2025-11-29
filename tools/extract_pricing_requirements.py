from pathlib import Path
from typing import Dict, Any, List

from utils.pdf_reader import read_pdf_text
from utils.docx_reader import read_docx_text
from utils.xlsx_reader import read_xlsx_text
from utils.clean_text import clean_text
from utils.classify_document import classify_document_type


KEYWORDS = [
    "pricing schedule",
    "price schedule",
    "bill of quantities",
    "boq",
    "pricing instructions",
    "fees and rates",
    "price list",
]


def _read_any(file_path: str) -> str:
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        return read_pdf_text(path)
    if suffix in (".doc", ".docx"):
        return read_docx_text(path)
    if suffix in (".xls", ".xlsx"):
        return read_xlsx_text(path)

    # Fallback to plain text
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def _extract_pricing_snippets(text: str) -> List[str]:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    snippets = []
    for i, line in enumerate(lines):
        lower = line.lower()
        if any(k in lower for k in KEYWORDS):
            window = lines[max(0, i - 3) : min(len(lines), i + 10)]
            snippets.append("\n".join(window))
    return snippets


def extract_pricing_requirements(file_path: str) -> Dict[str, Any]:
    """Core logic for `detect_pricing_requirements` MCP tool."""
    raw = _read_any(file_path)
    cleaned = clean_text(raw)
    doc_type = classify_document_type(cleaned)

    snippets = _extract_pricing_snippets(cleaned)
    excerpt = "\n\n".join(snippets[:5]) if snippets else cleaned[:4000]

    pricing_items = []
    # Very light heuristic: look for lines that look like an item + number
    for line in excerpt.splitlines():
        if any(ch.isdigit() for ch in line) and len(line) > 20:
            pricing_items.append(
                {
                    "raw_line": line.strip(),
                    "description_guess": line.strip()[:120],
                    "quantity_guess": None,
                    "unit_guess": None,
                }
            )

    result: Dict[str, Any] = {
        "instructions": (
            "You are a tender pricing assistant. The input document has been "
            f"classified as '{doc_type}'. Use the 'pricing_items' as a rough "
            "starting point only. Cross‑check everything against the original "
            "tender and ask the user to paste key sections (pricing schedule, "
            "BOQ, instructions) if they are not clearly visible here."
        ),
        "summary": f"Document appears to be a {doc_type} with "
        f"{len(pricing_items)} possible pricing‑related lines detected.",
        "currency": "ZAR",
        "pricing_items": pricing_items,
        "raw_text": excerpt,
        "file_path": file_path,
        "document_type": doc_type,
    }
    return result
