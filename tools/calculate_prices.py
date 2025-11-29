from typing import Dict, Any, List


def _calc_line(item: dict, vat_percent: float) -> dict:
    qty = float(item.get("quantity", 0) or 0)
    base_rate = float(item.get("base_rate", 0) or 0)
    markup = float(item.get("markup_percent", 0) or 0)

    rate_with_markup = base_rate * (1 + markup / 100.0)
    line_ex_vat = qty * rate_with_markup
    vat_amount = line_ex_vat * (vat_percent / 100.0)
    line_inc_vat = line_ex_vat + vat_amount

    out = dict(item)
    out.update(
        {
            "rate_with_markup": round(rate_with_markup, 2),
            "line_total_ex_vat": round(line_ex_vat, 2),
            "line_vat_amount": round(vat_amount, 2),
            "line_total_inc_vat": round(line_inc_vat, 2),
        }
    )
    return out


def calculate_prices(model_json: Dict[str, Any]) -> Dict[str, Any]:
    """Core logic for the `calculate` tool."""
    model = model_json.get("model", model_json)

    meta = model.get("meta", {})
    items: List[dict] = list(model.get("items", []))
    vat_percent = float(meta.get("vat_percent", 15.0) or 0)

    calc_items: List[dict] = []
    total_ex_vat = 0.0
    total_vat = 0.0
    total_inc_vat = 0.0

    for item in items:
        line = _calc_line(item, vat_percent)
        calc_items.append(line)
        total_ex_vat += line["line_total_ex_vat"]
        total_vat += line["line_vat_amount"]
        total_inc_vat += line["line_total_inc_vat"]

    totals = {
        "total_ex_vat": round(total_ex_vat, 2),
        "total_vat": round(total_vat, 2),
        "total_inc_vat": round(total_inc_vat, 2),
        "currency": meta.get("currency", "ZAR"),
        "vat_percent": vat_percent,
    }

    return {
        "instructions": (
            "This is a fully calculated pricing result. Present line items and totals "
            "neatly to the user. Emphasise that all pricing is indicative and must be "
            "verified against statutory requirements, tender rules, and the client's "
            "final approval before submission."
        ),
        "meta": meta,
        "items": calc_items,
        "totals": totals,
    }
