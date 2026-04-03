import json
from app.agents.climate import analyze_climate_impact
from app.agents.financial import analyze_market_trends
from app.agents.simulation import simulate_scenario
from app.agents.portfolio import optimize_portfolio
from app.agents.guard import validate_intent

print("--- Testing Climate Agent ---")
avoid_sectors = ["Fossil Fuels"]
climate_res = analyze_climate_impact(avoid_sectors)
print(json.dumps(climate_res, indent=2))

print("\n--- Testing Financial Agent ---")
financial_res = analyze_market_trends("moderate")
print(json.dumps(financial_res, indent=2))

print("\n--- Testing Portfolio Agent ---")
portfolio_res = optimize_portfolio(100000.0, climate_res, financial_res)
print(json.dumps(portfolio_res, indent=2))

print("\n--- Testing Simulation Agent ---")
simulation_res = simulate_scenario(100000.0, portfolio_res)
print(json.dumps(simulation_res, indent=2))

print("\n--- Testing Guard Agent ---")
# Mocking a trade that will violate multiple rules to see the guard in action!
trade = {
    "ticker": "XOM",
    "action": "buy",
    "quantity": 500,
    "sector": "Fossil Fuels",
    "estimated_cost": 80000.0,
    "risk_score": 90
}
guard_context = {
    "max_trade_size": 50000.0,
    "max_risk_threshold": 80,
    "max_allocation_pct": 0.20,
    "portfolio_value": 100000.0
}
guard_res = validate_intent(trade, avoid_sectors=avoid_sectors, context=guard_context)
print(json.dumps(guard_res, indent=2))