from app.agents.orchestrator import orchestrate

input_data = {
    "budget": 100000,
    "risk_level": "moderate",
    "max_trade": 50000,
    "avoid_sectors": []
}

result = orchestrate(input_data)

print(result["portfolio"])