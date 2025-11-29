from fastmcp import FastMCP

from tools.extract_pricing_requirements import extract_pricing_requirements
from tools.build_pricing_model import build_pricing_model
from tools.calculate_prices import calculate_prices
from tools.generate_html_report import generate_html_report
from tools.fetch_market_prices import fetch_market_prices
from tools.format_output import format_output

mcp = FastMCP("tri-tender-pricing-mcp")


@mcp.tool
def detect_pricing_requirements(file_path: str) -> dict:
    """
    Detect and extract pricing requirements from an uploaded tender document.

    Parameters
    ----------
    file_path: str
        Path to a local tender document (PDF, DOCX, XLSX).

    Returns
    -------
    dict
        {
          "instructions": "...LLM-ready description of what was found...",
          "summary": "...short natural language summary...",
          "currency": "ZAR",
          "pricing_items": [...],
          "raw_text": "cleaned text excerpt"
        }
    """
    return extract_pricing_requirements(file_path)


@mcp.tool
def build_model(description: str, tender_rules: str, company_rates: str) -> dict:
    """
    Build a structured pricing model JSON from free-text descriptions.

    - description: high-level description of what is being priced
    - tender_rules: pasted text or summary of pricing rules from the tender
    - company_rates: pasted baseline company rates (e.g. guard rates, hourly fees)

    Returns a JSON-serializable dict that can be edited by the LLM or user and
    passed to the `calculate` tool.
    """
    return build_pricing_model(description, tender_rules, company_rates)


@mcp.tool
def calculate(model_json: dict) -> dict:
    """
    Calculate final tender prices using Tri‑Tender Pricing Logic.

    Parameters
    ----------
    model_json: dict
        A structured model describing items, units, markups, VAT and options.

    Returns
    -------
    dict
        {
          "instructions": "...how to interpret this result...",
          "currency": "ZAR",
          "totals": {...},
          "items": [...]
        }
    """
    return calculate_prices(model_json)


@mcp.tool
def market_prices(item_name: str) -> dict:
    """
    Fetch (or simulate) external market prices to compare against tender pricing.

    This tool is intentionally simple and HTTP‑free by default so that it can
    run inside sandboxes. You can later extend it to call real APIs.

    Returns a dict with example price ranges and guidance for the LLM.
    """
    return fetch_market_prices(item_name)


@mcp.tool
def render_report(pricing_data: dict) -> dict:
    """
    Generate a full HTML pricing report document from pricing data.

    Parameters
    ----------
    pricing_data: dict
        Typically the output from `calculate`, possibly edited by the LLM.

    Returns
    -------
    dict
        {
          "mime_type": "text/html",
          "html": "<!DOCTYPE html>..."
        }
    """
    return generate_html_report(pricing_data)


@mcp.tool
def final_output(html: str) -> dict:
    """
    Wrap raw HTML into a standard Tri‑Tender output object that the
    Tri‑Tender desktop app can preview or convert to PDF.
    """
    return format_output(html)


if __name__ == "__main__":
    mcp.run()
