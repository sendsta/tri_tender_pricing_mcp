from typing import Dict


def format_output(html: str) -> Dict[str, str]:
    """
    Final thin wrapper used by the Tri‑Tender desktop / Dyad client.

    Some hosts prefer a consistent object structure when displaying HTML.
    This tool allows the LLM to send either raw HTML or the object returned
    from `render_report` and get back a simple, predictable format.
    """
    return {
        "mime_type": "text/html",
        "html": html,
        "instructions": (
            "Display this HTML in the Tri‑Tender preview pane or convert it to "
            "PDF for final downloading / submission."
        ),
    }
