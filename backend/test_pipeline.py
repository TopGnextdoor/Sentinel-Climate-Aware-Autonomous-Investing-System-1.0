from app.agents.master import run_pipeline

input_data = {
    "budget": 100000,
    "risk_level": "moderate",
    "max_trade": 50000,
    "avoid_sectors": ["fossil"]
}

import json

result = run_pipeline(**input_data)

print(json.dumps(result, indent=2))