from typing import Dict, Any
from app.services.trading_service import execute_alpaca_trade

def generate_trade_proposals(portfolio: Dict[str, Any], max_trade: float) -> Dict[str, Any]:
    """Agent for generating actual paper trades (Pre-Guard Intent Generation)."""
    return {
        "proposed_trade": {
            "ticker": "XOM", 
            "action": "buy", 
            "quantity": 150,
            "sector": "fossil",
            "risk_score": 60
        }, 
        "estimated_cost": 15000.0
    }

def execute_trade(trade: Dict[str, Any]) -> Dict[str, Any]:
    """Thin wrapper delegating to Alpaca service."""
    return execute_alpaca_trade(trade)
