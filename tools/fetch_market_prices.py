from typing import Dict, Any


def fetch_market_prices(item_name: str) -> Dict[str, Any]:
    """
    Simulated market price lookup.

    This is intentionally HTTP‑free so that the MCP can run in restricted
    environments (e.g. FastMCP Cloud). Once you have a host that permits
    outbound HTTP, you can extend this function to query real APIs for
    hardware, fuel, guarding wages, etc.
    """
    base_price = 1000.0
    suggestion = {
        "min_estimate": round(base_price * 0.7, 2),
        "max_estimate": round(base_price * 1.3, 2),
        "currency": "ZAR",
    }

    return {
        "instructions": (
            "These are rough, simulated market estimates for the given item. "
            "Use them only as a sanity‑check when comparing your tender pricing. "
            "Always prefer real supplier quotations or official wage tables."
        ),
        "item": item_name,
        "estimates": suggestion,
    }
