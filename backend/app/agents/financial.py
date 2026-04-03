from typing import Dict, Any
from app.services.risk import calculate_market_trends

def analyze_market_trends(risk_level: str) -> Dict[str, Any]:
    """Thin wrapper for assessing financial markets and trends."""
    return calculate_market_trends(risk_level)
