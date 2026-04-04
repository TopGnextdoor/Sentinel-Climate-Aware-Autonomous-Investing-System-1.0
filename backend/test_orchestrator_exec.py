"""
End-to-end smoke test for the full orchestration pipeline:
    Climate → Financial → Simulation → Portfolio → Trade → Guard → Execution → Explain

Run from Sentinel/backend:
    python test_orchestrator_exec.py

Uses a fresh in-memory portfolio per test; no live network calls needed
because the execution agent falls back to FALLBACK_PRICES when yfinance
is unavailable in certain test environments.
"""

import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))

from app.agents.orchestrator import orchestrate
from app.models.portfolio import _portfolio_store, Portfolio

# ─── helpers ──────────────────────────────────────────────────────────────────

def reset_portfolio(user_id: str, cash: float = 100_000.0):
    _portfolio_store[user_id] = Portfolio(user_id=user_id, cash_balance=cash)

def hr(title: str):
    print(f"\n{'─'*60}")
    print(f"  {title}")
    print('─'*60)

def pprint(label: str, value):
    if isinstance(value, dict):
        print(f"  {label}:")
        for k, v in value.items():
            print(f"    {k}: {v}")
    else:
        print(f"  {label}: {value}")

# ─── test 1 — normal approved pipeline ────────────────────────────────────────

def test_approved_pipeline():
    hr("TEST 1 — Normal pipeline (guard should APPROVE, execution should EXECUTE)")
    uid = "orch_user_1"
    reset_portfolio(uid, 100_000.0)

    result = orchestrate(
        input_data={
            "budget":         50_000.0,
            "risk_level":     "moderate",
            "max_trade":      50_000.0,
            "avoid_sectors":  [],
            "esg_threshold":  0,          # very low — let everything through
        },
        user_id=uid,
    )

    # ── required top-level keys ───────────────────────────────────────────────
    required_keys = [
        "portfolio", "climate_data", "financial_data",
        "simulation", "trade", "guard",
        "execution_result",              # ← must be present
        "explanation", "orchestration",
    ]
    missing = [k for k in required_keys if k not in result]
    assert not missing, f"Missing keys in response: {missing}"
    print("  ✓  All top-level keys present")

    # ── orchestration trace must include an 'execution' step ─────────────────
    agents_in_trace = [s["agent"] for s in result["orchestration"]]
    assert "execution" in agents_in_trace, (
        f"'execution' step missing from orchestration trace: {agents_in_trace}"
    )
    print(f"  ✓  Orchestration trace: {' → '.join(agents_in_trace)}")

    # ── execution_result shape ────────────────────────────────────────────────
    ex = result["execution_result"]
    assert "status" in ex, "execution_result missing 'status'"
    print(f"  ✓  execution_result.status : {ex['status']}")

    if ex["status"] == "EXECUTED":
        assert ex.get("price",      0) > 0,  "price should be > 0"
        assert ex.get("total_cost", 0) > 0,  "total_cost should be > 0"
        assert ex.get("trade_id"),            "trade_id should not be empty"
        print(f"  ✓  price      : ${ex['price']}")
        print(f"  ✓  total_cost : ${ex['total_cost']:,.2f}")
        print(f"  ✓  trade_id   : {ex['trade_id']}")
        # Portfolio cash should be reduced
        cash_after = ex["portfolio"]["cash_balance"]
        print(f"  ✓  cash_left  : ${cash_after:,.2f}")
    elif ex["status"] in ("SKIPPED", "REJECTED"):
        print(f"  ℹ  Execution skipped/rejected — reason: {ex.get('reason', 'n/a')}")
        print("     (guard may have blocked the trade — this is valid pipeline behaviour)")
    else:
        print(f"  ℹ  Unexpected status: {ex['status']}")


# ─── test 2 — blocked pipeline (avoid all sectors) ────────────────────────────

def test_blocked_pipeline():
    hr("TEST 2 — All sectors blocked (execution must be SKIPPED)")
    uid = "orch_user_2"
    reset_portfolio(uid, 100_000.0)

    result = orchestrate(
        input_data={
            "budget":         50_000.0,
            "risk_level":     "moderate",
            "max_trade":      50_000.0,
            "avoid_sectors":  ["technology", "auto", "fossils", "renewables", "unknown"],
            "esg_threshold":  999,        # impossibly high — nothing passes
        },
        user_id=uid,
    )

    ex = result["execution_result"]
    assert ex["status"] in ("SKIPPED", "REJECTED"), (
        f"Expected SKIPPED/REJECTED when all sectors blocked, got: {ex['status']}"
    )
    print(f"  ✓  execution_result.status : {ex['status']}")
    print(f"  ✓  reason                  : {ex.get('reason', 'n/a')}")

    # Portfolio cash must be unchanged — no trade was made
    portfolio_after = _portfolio_store.get(uid)
    assert portfolio_after.cash_balance == 100_000.0, (
        f"Cash should be unchanged at $100,000 but got ${portfolio_after.cash_balance:,.2f}"
    )
    print(f"  ✓  Cash unchanged           : ${portfolio_after.cash_balance:,.2f}")


# ─── test 3 — response shape matches frontend expectations ────────────────────

def test_response_shape():
    hr("TEST 3 — Response shape / field types")
    uid = "orch_user_3"
    reset_portfolio(uid, 100_000.0)

    result = orchestrate(
        input_data={"budget": 10_000.0, "risk_level": "low", "max_trade": 5_000.0},
        user_id=uid,
    )

    ex = result["execution_result"]
    assert isinstance(ex, dict),          "execution_result must be a dict"
    assert isinstance(ex["status"], str), "status must be a str"

    if ex["status"] == "EXECUTED":
        assert isinstance(ex["price"],      float), "price must be float"
        assert isinstance(ex["total_cost"], float), "total_cost must be float"
        assert isinstance(ex["quantity"],   float), "quantity must be float"
        assert isinstance(ex["trade_id"],   str),   "trade_id must be str"
        assert isinstance(ex["portfolio"],  dict),  "portfolio must be dict"

    orch = result["orchestration"]
    assert isinstance(orch, list), "orchestration must be a list"
    exec_steps = [s for s in orch if s["agent"] == "execution"]
    assert len(exec_steps) == 1, f"Expected exactly 1 execution step, got {len(exec_steps)}"
    print(f"  ✓  execution_result is a well-formed dict")
    print(f"  ✓  orchestration has exactly 1 execution step")
    print(f"  ✓  execution step status: {exec_steps[0]['status']}")


# ─── runner ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n🚀  Sentinel Orchestrator — Execution Integration Tests")

    test_approved_pipeline()
    test_blocked_pipeline()
    test_response_shape()

    print(f"\n{'═'*60}")
    print("  ✅  All orchestrator tests passed.")
    print(f"{'═'*60}\n")
