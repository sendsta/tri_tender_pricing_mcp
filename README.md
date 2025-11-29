# Tri‑Tender Pricing MCP

This is a production‑ready **Model Context Protocol (MCP)** server built with
[FastMCP](https://gofastmcp.com/) for **Tri‑Tender**. It focuses on
**pricing schedules for tenders and RFQs**.

The server exposes tools that:

1. Detect and extract pricing requirements from tender packs
2. Build a structured pricing model from tender rules + company rates
3. Calculate final prices (including markups & VAT)
4. Optionally compare against market prices
5. Generate a styled HTML pricing report ready for PDF export
6. Wrap the output in a Tri‑Tender‑friendly format for preview


## 1. Project Structure

```bash
tri_tender_pricing_mcp/
├── server.py
├── requirements.txt
├── README.md
├── tools/
│   ├── extract_pricing_requirements.py
│   ├── build_pricing_model.py
│   ├── calculate_prices.py
│   ├── generate_html_report.py
│   ├── fetch_market_prices.py
│   └── format_output.py
├── utils/
│   ├── pdf_reader.py
│   ├── docx_reader.py
│   ├── xlsx_reader.py
│   ├── classify_document.py
│   └── clean_text.py
└── resources/
    ├── pricing_templates/
    │   ├── base_template.html
    │   ├── table_style.css
    │   └── branding.css
    └── sample_data/
        └── example_pricing.json
```


## 2. Installation

Create and activate a virtual environment (recommended), then:

```bash
pip install -r requirements.txt
```

Verify that FastMCP is installed:

```bash
fastmcp version
```


## 3. Running the MCP Server

```bash
fastmcp run server.py
```

By default FastMCP will use stdio for transport. Some hosts also support:

```bash
python server.py
```

or

```bash
fastmcp run --transport sse --host 0.0.0.0 --port 8000 server.py
```

(Consult the FastMCP docs / your host's docs if you want SSE or HTTP.)


## 4. Registering in Tri‑Tender (Desktop / Dyad)

Use a configuration entry like this in your MCP client:

```jsonc
{
  "mcpServers": {
    "tri_tender_pricing_mcp": {
      "command": "python",
      "args": ["server.py"],
      "env": {}
    }
  }
}
```

If you deploy it remotely with SSE/HTTP, you can instead use:

```jsonc
{
  "mcpServers": {
    "tri_tender_pricing_mcp": {
      "url": "http://YOUR-HOST:8000/sse"
    }
  }
}
```


## 5. Exposed Tools

### `detect_pricing_requirements(file_path: str) -> dict`

- Reads PDF, DOCX or XLSX
- Cleans the text
- Classifies the document type (tender, pricing schedule, BOQ, etc.)
- Tries to extract pricing‑related sections
- Returns:
  - `instructions` (LLM‑ready description of what was found)
  - `summary`
  - `currency`
  - `pricing_items` (rough skeleton list)
  - `raw_text` (trimmed excerpt for the LLM)


### `build_model(description: str, tender_rules: str, company_rates: str) -> dict`

- Takes free‑text input and produces a **structured pricing model** with:
  - `items`: description, unit, quantity, base_rate, markup_percent
  - `meta`: currency, VAT %, assumptions


### `calculate(model_json: dict) -> dict`

- Applies line‑level calculations:
  - `line_total_ex_vat`
  - `line_vat_amount`
  - `line_total_inc_vat`
- Sums to grand totals
- Returns `items` + `totals` + `instructions` for the LLM.


### `market_prices(item_name: str) -> dict`

- Currently returns **simulated** market prices.
- Designed to be extended with real HTTP APIs (hardware, fuel, etc.).


### `render_report(pricing_data: dict) -> dict`

- Renders a styled HTML report based on `resources/pricing_templates/base_template.html`
- Returns: `{ "mime_type": "text/html", "html": "..." }`


### `final_output(html: str) -> dict`

- Final simple wrapper used by Tri‑Tender desktop app / Dyad templates.


## 6. Customisation

- Update `resources/pricing_templates/base_template.html` and CSS files
  to match Tri‑Tender branding.
- Extend the logic in `calculate_prices.py` to support:
  - multi‑year escalations
  - different markups per category
  - PSIRA / industry‑regulated minimums
- Plug real HTTP APIs into `fetch_market_prices.py` once you have a
  host that allows outbound HTTP.


## 7. Safety Notes

- This server does **no** remote network calls by default.
- All calculations are purely local and deterministic.
- Perfect for running inside constrained MCP hosts (FastMCP Cloud,
  Cursor, Claude Desktop, etc.).
