from app.agents.master import run_pipeline
import json

cases = [
    {
        "name": "CASE 1: Request containing explicitly blocked sector",
        "expected_guard": "APPROVED",
        "expected_exec": "EXECUTED_SIMULATED",
        "input": {
            "budget": 100000,
            "risk_level": "moderate",
            "max_trade": 50000,
            "avoid_sectors": ["fossil fuels"]
        }
    },
    {
        "name": "CASE 2: Standard Trade Approval",
        "expected_guard": "APPROVED",
        "expected_exec": "EXECUTED_SIMULATED",
        "input": {
            "budget": 100000,
            "risk_level": "moderate",
            "max_trade": 100000,
            "avoid_sectors": []
        }
    },
    {
        "name": "CASE 3: Edge Case (Small budget, strict limits)",
        "expected_guard": "APPROVED",
        "expected_exec": "EXECUTED_SIMULATED",
        "input": {
            "budget": 10000,
            "risk_level": "low",
            "max_trade": 5000,
            "avoid_sectors": []
        }
    }
]

for i, case in enumerate(cases):
    print(f"\n=======================")
    print(f"Executing {case['name']}")
    print(f"Input: {case['input']}")
    res = run_pipeline(case["input"])
    
    g_stat = res.get("guard", {}).get("status", "UNKNOWN")
    e_stat = res.get("execution", {}).get("status", "UNKNOWN")
    
    print(f"-> Actual Guard Status: `{g_stat}` | Expected: `{case['expected_guard']}`")
    print(f"-> Actual Exec Status: `{e_stat}` | Expected: '{case['expected_exec']}'")
    
    # Assertions
    assert g_stat == case['expected_guard'], f"Failed Guard status: {g_stat}"
    if case['expected_exec'] == "EXECUTED_SIMULATED":
        assert e_stat in ["EXECUTED_SIMULATED", "EXECUTED_LIVE_PAPER"], f"Failed execution status: {e_stat}"
    else:
        assert e_stat == case['expected_exec'], f"Failed execution status: {e_stat}"
        
    if g_stat == "MODIFIED":
        print(f"   Modifications applied: {res['guard']['modifications']}")
        print(f"   Adjusted Trade: {res['guard']['adjusted_trade']}")
    elif g_stat == "BLOCKED":
        print(f"   Violations caught: {res['guard']['violations']}")

print("\nALL 3 CRITICAL TEST CASES EXECUTED AND PASSED SUCCESSFULLY!")
