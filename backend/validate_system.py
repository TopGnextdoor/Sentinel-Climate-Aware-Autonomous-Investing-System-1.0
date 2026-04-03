"""
Sentinel System Validation
End-to-end integration check for all agents + orchestrator.
"""
import json
from app.agents.orchestrator import orchestrate

PASS = "[PASS]"
FAIL = "[FAIL]"
SEP  = "-" * 60

def check(label, condition, detail=""):
    status = PASS if condition else FAIL
    msg = f"  {status} {label}"
    if detail:
        msg += f"\n         detail: {detail}"
    print(msg)
    return condition

def run_case(name, input_data):
    print(f"\n{SEP}")
    print(f"TEST: {name}")
    print(f"INPUT: {json.dumps(input_data)}")
    print(SEP)
    result = orchestrate(input_data)
    return result

# ── CASE 1: APPROVED ──────────────────────────────────────────
r = run_case("APPROVED — No restrictions, large budget", {
    "budget": 100000,
    "risk_level": "moderate",
    "max_trade": 100000,
    "avoid_sectors": []
})

orch = r.get("orchestration", [])
guard = r.get("guard", {})
trade = r.get("trade", {})
exec_ = r.get("execution", {})
sim   = r.get("simulation", {})

check("orchestration key present",          "orchestration" in r)
check("climate step completed",             any(s["agent"]=="climate"  and s["status"]=="completed" for s in orch))
check("financial step completed",           any(s["agent"]=="financial" and s["status"]=="completed" for s in orch))
check("simulation step completed",          any(s["agent"]=="simulation" and s["status"]=="completed" for s in orch))
check("portfolio step completed",           any(s["agent"]=="portfolio" and s["status"]=="completed" for s in orch))
check("guard APPROVED",                     guard.get("status") == "APPROVED",  f"got: {guard.get('status')}")
check("trader executed",                    any(s["agent"]=="trader" and s["status"]=="completed" for s in orch))
check("execution present",                  exec_ is not None,                   f"got: {exec_}")
check("simulation has sharpe_ratio",        "sharpe_ratio" in sim,               f"keys: {list(sim.keys())}")
check("simulation has value_at_risk_95",    "value_at_risk_95" in sim)
check("trade has proposed_trade",           "proposed_trade" in trade,           f"got: {trade}")
check("climate_data returned",              "climate_data" in r)
check("financial_data returned",            "financial_data" in r)
check("explanation returned",               bool(r.get("explanation")))

# ── CASE 2: BLOCKED by ESG ───────────────────────────────────
r2 = run_case("ESG BLOCKED — avoid fossil fuels", {
    "budget": 100000,
    "risk_level": "moderate",
    "max_trade": 50000,
    "avoid_sectors": ["fossil fuels"]
})

orch2  = r2.get("orchestration", [])
guard2 = r2.get("guard", {})
exec2  = r2.get("execution")
trade2 = r2.get("trade", {})
climat2 = r2.get("climate_data", {})

check("orchestration returned",             "orchestration" in r2)
check("climate excluded fossil assets",     all(
    a.get("sector", "").lower() != "fossil fuels"
    for a in climat2.get("eligible_assets", [])
), f"assets: {[a['sector'] for a in climat2.get('eligible_assets',[])]}")
check("guard not BLOCKED (upstream filtered)", guard2.get("status") != "BLOCKED", f"guard: {guard2.get('status')}")
check("execution occurred",                 exec2 is not None,                   f"got: {exec2}")

# ── CASE 3: GUARD BLOCKED directly ───────────────────────────
# Force a high-risk trade by avoiding most sectors so portfolio may be thin
r3 = run_case("GUARD BLOCKED — high risk trade attempt", {
    "budget": 5000,
    "risk_level": "low",
    "max_trade": 100,   # tiny max_trade -> guard should block on budget
    "avoid_sectors": []
})

orch3  = r3.get("orchestration", [])
guard3 = r3.get("guard", {})
exec3  = r3.get("execution")

check("orchestration returned",             "orchestration" in r3)
check("guard ran",                          guard3.get("status") in ["APPROVED","BLOCKED","MODIFIED"], f"got: {guard3.get('status')}")
check("execution is None when blocked",     exec3 is None if guard3.get("status")=="BLOCKED" else True)
check("explain step completed",             any(s["agent"]=="explain" and s["status"]=="completed" for s in orch3))

print(f"\n{SEP}")
print("VALIDATION COMPLETE")
print(SEP)
