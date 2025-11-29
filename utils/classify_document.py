from typing import Literal


def classify_document_type(text: str) -> str:
    """
    Very lightweight document classifier for tender content.

    This is deterministic and does not call any models. It only uses keyword
    heuristics to help the LLM reason about what kind of file was uploaded.
    """
    t = text.lower()

    if "request for quotation" in t or "rfq" in t:
        return "RFQ (Request for Quotation)"
    if "request for proposal" in t or "rfp" in t:
        return "RFP (Request for Proposal)"
    if "invitation to bid" in t or "tender no" in t or "bid number" in t:
        return "Tender / RFB"
    if "bill of quantities" in t or "boq" in t:
        return "Bill of Quantities / Pricing Schedule"
    if "pricing schedule" in t or "price schedule" in t:
        return "Pricing Schedule"
    if "terms and conditions" in t:
        return "Terms & Conditions"

    return "Procurement‑related document"
