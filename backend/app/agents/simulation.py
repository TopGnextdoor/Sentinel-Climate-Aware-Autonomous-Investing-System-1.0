from typing import Dict, Any
from app.services.simulation_engine import run_monte_carlo_sim

def simulate_scenario(budget: float, portfolio: Dict[str, Any]) -> Dict[str, Any]:
    """Thin wrapper for running potential trade simulations."""
    budget = budget or 10000.0
    
    # Portfolio extraction rules logic here
    portfolio_volatility = 0.12 
    portfolio_return = 0.07 
    
    return run_monte_carlo_sim(budget, portfolio_return, portfolio_volatility)
