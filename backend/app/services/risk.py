from typing import Dict, Any
import random

def calculate_market_trends(risk_level: str) -> Dict[str, Any]:
    """Math calculations for predicted returns, volatility indexing, and scoring."""
    risk = risk_level.lower() if risk_level else "moderate"
    
    if risk == "low":
        expected_return = 0.04
        volatility = 0.05
        market_sentiment = "stable"
    elif risk == "high":
        expected_return = 0.12
        volatility = 0.18
        market_sentiment = "volatile"
    else:
        expected_return = 0.08
        volatility = 0.10
        market_sentiment = "cautiously optimistic"
        
    expected_return += random.uniform(-0.01, 0.01)
    
    return {
        "market_sentiment": market_sentiment,
        "recommended_risk": risk_level or "Moderate",
        "expected_return": round(expected_return, 4),
        "volatility": round(volatility, 4),
        "market_risk_score": round(volatility * 100, 2)
    }
