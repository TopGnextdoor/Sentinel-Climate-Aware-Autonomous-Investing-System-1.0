import json
import os
from typing import Dict, Any

def get_stock_prices() -> Dict[str, float]:
    """Retrieve sample stock prices from JSON."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    stocks_path = os.path.join(base_dir, "data", "sample_stocks.json")
    
    stock_prices = {}
    if os.path.exists(stocks_path):
        with open(stocks_path, "r") as f:
            for item in json.load(f):
                stock_prices[item["ticker"]] = item["price"]
    return stock_prices
