from typing import Dict, Any, List


def _parse_company_rates(company_rates: str) -> List[dict]:
    """
    Parse simplistic CSV‑style lines from the company rate sheet.

    Expected loose format per line (very forgiving):
        description, unit_cost, unit, default_quantity

    Example:
        Security Guard Grade C, 22.50, hour, 720
    """
    items = []
    for raw_line in company_rates.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 2:
            continue

        description = parts[0]
        try:
            unit_cost = float(parts[1])
        except ValueError:
            continue

        unit = parts[2] if len(parts) > 2 and parts[2] else "unit"
        try:
            default_qty = float(parts[3]) if len(parts) > 3 and parts[3] else 1.0
        except ValueError:
            default_qty = 1.0

        items.append(
            {
                "description": description,
                "unit": unit,
                "quantity": default_qty,
                "base_rate": unit_cost,
                "markup_percent": 25.0,
            }
        )
    return items


def build_pricing_model(description: str, tender_rules: str, company_rates: str) -> Dict[str, Any]:
    """
    Build a structured pricing model JSON for the `calculate` tool.

    This function is intentionally deterministic and light‑weight. The
    surrounding LLM can refine the resulting structure (add/remove items,
    change markups, etc.).
    """
    items = _parse_company_rates(company_rates)

    model: Dict[str, Any] = {
        "meta": {
            "description": description.strip() or "Tender pricing model",
            "tender_rules": tender_rules.strip(),
            "currency": "ZAR",
            "vat_percent": 15.0,
            "default_markup_percent": 25.0,
            "notes": (
                "This is a base pricing model created by the Tri‑Tender Pricing MCP. "
                "The LLM and the human user should carefully confirm all quantities, "
                "units, mark‑ups and any PSIRA / statutory requirements before use."
            ),
        },
        "items": items,
    }

    return {
        "instructions": (
            "You now have a structured pricing model under the 'model' key. "
            "You may modify 'items' (quantities, markups, descriptions) as needed "
            "and then send the updated 'model' value directly into the `calculate` tool."
        ),
        "model": model,
    }
