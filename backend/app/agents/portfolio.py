from typing import Dict, Any
from app.services.optimizer import calculate_allocation
from app.services.market_data import get_stock_prices

def optimize_portfolio(budget: float, climate_data: Dict[str, Any], financial_data: Dict[str, Any]) -> Dict[str, Any]:
    """Thin wrapper for optimizing portfolio mixes."""
    budget = budget or 10000.0
    eligible_assets = climate_data.get("eligible_assets", [])
    
    # Delegate to external market data service
    stock_prices = get_stock_prices()
    
    # Delegate to mathematical optimization service
    return calculate_allocation(budget, eligible_assets, stock_prices)
