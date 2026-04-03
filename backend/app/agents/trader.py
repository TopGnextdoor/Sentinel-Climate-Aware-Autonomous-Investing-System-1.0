from typing import Dict, Any
from app.services.trading_service import execute_alpaca_trade
import random

def generate_trade_proposals(portfolio: Dict[str, Any], max_trade: float) -> Dict[str, Any]:
    """Agent for generating actual paper trades (Pre-Guard Intent Generation)."""
    # Meta data mapping to test Guard Rules dynamically
    ticker_meta = {
        "AAPL": {"sector": "technology", "risk_score": 30, "price": 175.50},
        "MSFT": {"sector": "technology", "risk_score": 25, "price": 405.10},
        "TSLA": {"sector": "auto", "risk_score": 60, "price": 180.20},
        "XOM": {"sector": "fossils", "risk_score": 85, "price": 105.30},
        "NEE": {"sector": "renewables", "risk_score": 20, "price": 70.00}
    }
    
    # Dynamically pick a target to demonstrate varied Guard Decisions
    target_ticker = random.choice(list(ticker_meta.keys()))
    meta = ticker_meta[target_ticker]
    
    # Calculate a valid quantity based on max_trade budget context
    price = meta["price"]
    affordable_qty = max(1, int((max_trade * 0.5) / price)) 
    quantity = min(affordable_qty, 200) # cap at 200 shares
    
    estimated_cost = quantity * price

    return {
        "proposed_trade": {
            "ticker": target_ticker, 
            "action": "buy", 
            "quantity": quantity,
            "sector": meta["sector"],
            "risk_score": meta["risk_score"]
        }, 
        "estimated_cost": round(estimated_cost, 2)
    }

def execute_trade(trade: Dict[str, Any]) -> Dict[str, Any]:
    """Thin wrapper delegating to Alpaca service."""
    return execute_alpaca_trade(trade)
