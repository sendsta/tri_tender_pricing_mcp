from pathlib import Path
from typing import Dict, Any, List


def _load_template() -> str:
    base_dir = Path(__file__).resolve().parents[1]
    template_path = base_dir / "resources" / "pricing_templates" / "base_template.html"
    try:
        return template_path.read_text(encoding="utf-8")
    except Exception:
        # Simple fallback template
        return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>{{REPORT_TITLE}}</title>
  <style>
    body { font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background:#f9fafb; color:#0b1120; padding:32px; }
    .page { max-width: 960px; margin: 0 auto; background:#ffffff; border-radius:16px; padding:32px; box-shadow:0 10px 40px rgba(15,23,42,0.08); }
    h1 { font-size: 28px; margin-bottom:4px; }
    h2 { margin-top:32px; margin-bottom:8px; font-size:20px; }
    table { width:100%; border-collapse:collapse; margin-top:12px; font-size:14px; }
    th, td { border:1px solid #e5e7eb; padding:8px 10px; text-align:left; }
    th { background:#f3f4f6; }
    tfoot td { font-weight:600; }
    .badge { display:inline-block; padding:4px 10px; border-radius:999px; font-size:11px; background:#eff6ff; color:#1d4ed8; }
    .meta-grid { display:grid; grid-template-columns: repeat(auto-fit,minmax(180px,1fr)); gap:8px 24px; font-size:13px; margin-top:8px; }
    .meta-label { font-weight:600; color:#6b7280; }
    .meta-value { color:#111827; }
  </style>
</head>
<body>
  <div class="page">
    <header>
      <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:16px;">
        <div>
          <h1>{{REPORT_TITLE}}</h1>
          <div class="badge">Tri‑Tender · Pricing Report</div>
        </div>
        <div style="text-align:right; font-size:12px; color:#6b7280;">
          <div>Currency: {{CURRENCY}}</div>
          <div>VAT: {{VAT_PERCENT}}%</div>
        </div>
      </div>
    </header>

    <section style="margin-top:24px;">
      <h2>Overview</h2>
      <p style="font-size:14px;">{{SUMMARY}}</p>
      <div class="meta-grid">
        <div>
          <div class="meta-label">Description</div>
          <div class="meta-value">{{DESCRIPTION}}</div>
        </div>
        <div>
          <div class="meta-label">Notes</div>
          <div class="meta-value">{{NOTES}}</div>
        </div>
      </div>
    </section>

    <section style="margin-top:24px;">
      <h2>Pricing Breakdown</h2>
      {{PRICING_TABLE}}
    </section>

    <section style="margin-top:24px; font-size:12px; color:#6b7280;">
      <p>
        Disclaimer: This pricing schedule was generated with assistance from the
        Tri‑Tender Pricing MCP. All figures are indicative only and must be
        reviewed, confirmed, and approved by a qualified human decision‑maker
        before submission to any client or organ of state.
      </p>
    </section>
  </div>
</body>
</html>
"""


def _render_table(items: List[dict], totals: Dict[str, Any]) -> str:
    headers = [
        "Description",
        "Unit",
        "Qty",
        "Base Rate",
        "Markup %",
        "Rate w/ Markup",
        "Line Total (ex VAT)",
        "VAT",
        "Line Total (inc VAT)",
    ]

    def fmt(v):
        if isinstance(v, (int, float)):
            return f"{v:,.2f}"
        return str(v) if v is not None else ""

    rows_html = ""
    for it in items:
        rows_html += "<tr>" + "".join(
            f"<td>{fmt(col)}</td>"
            for col in [
                it.get("description", ""),
                it.get("unit", ""),
                it.get("quantity", ""),
                it.get("base_rate", ""),
                it.get("markup_percent", ""),
                it.get("rate_with_markup", ""),
                it.get("line_total_ex_vat", ""),
                it.get("line_vat_amount", ""),
                it.get("line_total_inc_vat", ""),
            ]
        ) + "</tr>"

    foot_html = f"""
    <tr>
      <td colspan="6" style="text-align:right; font-weight:600;">Total ex VAT</td>
      <td>{fmt(totals.get("total_ex_vat", 0))}</td>
      <td>{fmt(totals.get("total_vat", 0))}</td>
      <td>{fmt(totals.get("total_inc_vat", 0))}</td>
    </tr>
    """

    table_html = f"""
    <table>
      <thead>
        <tr>{''.join(f'<th>{h}</th>' for h in headers)}</tr>
      </thead>
      <tbody>
        {rows_html}
      </tbody>
      <tfoot>
        {foot_html}
      </tfoot>
    </table>
    """
    return table_html


def generate_html_report(pricing_data: Dict[str, Any]) -> Dict[str, Any]:
    meta = pricing_data.get("meta", {})
    items = pricing_data.get("items", [])
    totals = pricing_data.get("totals", {})

    template = _load_template()

    pricing_table = _render_table(items, totals)

    html = (
        template
        .replace("{{REPORT_TITLE}}", "Tri‑Tender Pricing Schedule")
        .replace("{{CURRENCY}}", str(totals.get("currency", "ZAR")))
        .replace("{{VAT_PERCENT}}", str(totals.get("vat_percent", meta.get("vat_percent", 15))))
        .replace("{{SUMMARY}}", pricing_data.get("instructions", "Tender pricing schedule."))
        .replace("{{DESCRIPTION}}", meta.get("description", ""))
        .replace("{{NOTES}}", meta.get("notes", ""))
        .replace("{{PRICING_TABLE}}", pricing_table)
    )

    return {
        "mime_type": "text/html",
        "html": html,
    }
