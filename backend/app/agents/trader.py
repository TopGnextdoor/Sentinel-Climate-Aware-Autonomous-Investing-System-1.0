from typing import Dict, Any
from app.services.trading_service import execute_alpaca_trade
import random

def generate_trade_proposals(allowed_assets: list, max_trade: float) -> Dict[str, Any]:
    """Agent for generating actual paper trades (Pre-Guard Intent Generation)."""
    ticker_meta = {
        "AAPL": {"sector": "technology", "risk_score": 30},
        "MSFT": {"sector": "technology", "risk_score": 25},
        "TSLA": {"sector": "auto", "risk_score": 60},
        "XOM": {"sector": "fossils", "risk_score": 85},
        "NEE": {"sector": "renewables", "risk_score": 20}
    }
    
    if not allowed_assets:
        # Fallback if somehow empty, but theoretically upstream filters it
        allowed_assets = ["AAPL"]
        
    target_ticker = random.choice(allowed_assets)
    # Ensure meta fallback if ticker randomly selected isn't in test meta map
    meta = ticker_meta.get(target_ticker, {"sector": "unknown", "risk_score": 50})
    
    # Calculate a valid quantity based on max_trade budget context
    # Need to fetch live price!
    from app.services.market_data import get_stock_price
    price = get_stock_price(target_ticker)
    
    affordable_qty = max(1, int((max_trade * 0.5) / price)) 
    quantity = min(affordable_qty, 200) # cap at 200 shares
    
    estimated_cost = quantity * price

    return {
        "proposed_trade": {
            "ticker": target_ticker, 
            "action": "buy", 
            "quantity": quantity,
            "sector": meta["sector"],
            "risk_score": meta["risk_score"],
            "price": round(price, 2)
        }, 
        "estimated_cost": round(estimated_cost, 2)
    }

def execute_trade(trade: Dict[str, Any]) -> Dict[str, Any]:
    """Thin wrapper delegating to Alpaca service."""
    return execute_alpaca_trade(trade)
