from app.agents.portfolio import optimize_portfolio

# Mock data to simulate upstream agents
climate_data = {
    "eligible_assets": [
        {"ticker": "AAPL", "climate_score": 85, "risk_level": "moderate"},
        {"ticker": "MSFT", "climate_score": 75, "risk_level": "moderate"},
        {"ticker": "TSLA", "climate_score": 90, "risk_level": "high"}
    ]
}
financial_data = {}
budget = 100000.0

portfolio = optimize_portfolio(budget, climate_data, financial_data)

print(portfolio)