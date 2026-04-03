from typing import Dict, Any, List, Optional
from app.services.risk import calculate_market_trends

def analyze_market_trends(risk_level: str, tickers: Optional[List[str]] = None) -> Dict[str, Any]:
    """Thin wrapper for assessing financial markets and trends using real market signals."""
    return calculate_market_trends(risk_level, tickers=tickers)
