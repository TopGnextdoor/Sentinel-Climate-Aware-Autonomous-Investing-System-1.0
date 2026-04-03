from app.agents.orchestrator import orchestrate

input_data = {
    "budget": 100000,
    "risk_level": "high",
    "max_trade": 100000,
    "avoid_sectors": []
}

result = orchestrate(input_data)

print(result)