"""
Smoke test for backend/app/agents/execution.py
Run from the Sentinel/backend directory:
    python test_execution.py

Uses price_override so no live network call is made.
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app.agents.execution import run_execution
from app.models.portfolio import _portfolio_store, Portfolio

# ─── Helpers ──────────────────────────────────────────────────────────────────

def reset(user_id: str, cash: float = 100_000.0):
    """Provision a fresh portfolio for the test user."""
    _portfolio_store[user_id] = Portfolio(user_id=user_id, cash_balance=cash)


def hr(title: str):
    print(f"\n{'─'*55}")
    print(f"  {title}")
    print('─'*55)


# ─── Tests ────────────────────────────────────────────────────────────────────

def test_buy_success():
    hr("TEST 1 — BUY 100 × AAPL @ $190.23")
    reset("u1")
    result = run_execution("u1", "AAPL", "BUY", 100, price_override=190.23)

    assert result["status"]     == "EXECUTED",  f"bad status: {result['status']}"
    assert result["action"]     == "BUY"
    assert result["ticker"]     == "AAPL"
    assert result["price"]      == 190.23
    assert result["total_cost"] == 19023.0
    expected_cash = round(100_000.0 - 19023.0, 2)
    assert result["portfolio"]["cash_balance"] == expected_cash, (
        f"Expected cash {expected_cash}, got {result['portfolio']['cash_balance']}"
    )
    print(f"  ✓  status      : {result['status']}")
    print(f"  ✓  price       : ${result['price']}")
    print(f"  ✓  total_cost  : ${result['total_cost']}")
    print(f"  ✓  cash_left   : ${result['portfolio']['cash_balance']:,.2f}")
    print(f"  ✓  trade_id    : {result['trade_id']}")


def test_sell_success():
    hr("TEST 2 — SELL 50 × AAPL @ $200.00  (after buying 100)")
    reset("u2")
    run_execution("u2", "AAPL", "BUY",  100, price_override=190.23)
    result = run_execution("u2", "AAPL", "SELL", 50, price_override=200.00)

    assert result["status"]     == "EXECUTED"
    assert result["action"]     == "SELL"
    assert result["total_cost"] == 10_000.0
    # cash after buy  = 100000 - 19023 = 80977
    # cash after sell =  80977 + 10000 = 90977
    assert result["portfolio"]["cash_balance"] == 90977.0, (
        f"Unexpected cash: {result['portfolio']['cash_balance']}"
    )
    print(f"  ✓  status      : {result['status']}")
    print(f"  ✓  proceeds    : ${result['total_cost']}")
    print(f"  ✓  cash_now    : ${result['portfolio']['cash_balance']:,.2f}")


def test_insufficient_funds():
    hr("TEST 3 — BUY with insufficient cash  (expect ValueError)")
    reset("u3", cash=100.0)   # only $100
    try:
        run_execution("u3", "AAPL", "BUY", 10, price_override=190.23)
        print("  ✗  Should have raised ValueError!")
        sys.exit(1)
    except ValueError as e:
        print(f"  ✓  Correctly rejected: {e}")


def test_insufficient_shares():
    hr("TEST 4 — SELL more shares than held  (expect ValueError)")
    reset("u4")
    run_execution("u4", "AAPL", "BUY", 5, price_override=190.23)
    try:
        run_execution("u4", "AAPL", "SELL", 999, price_override=190.23)
        print("  ✗  Should have raised ValueError!")
        sys.exit(1)
    except ValueError as e:
        print(f"  ✓  Correctly rejected: {e}")


def test_sell_no_position():
    hr("TEST 5 — SELL with zero position  (expect ValueError)")
    reset("u5")
    try:
        run_execution("u5", "MSFT", "SELL", 1, price_override=402.11)
        print("  ✗  Should have raised ValueError!")
        sys.exit(1)
    except ValueError as e:
        print(f"  ✓  Correctly rejected: {e}")


def test_invalid_action():
    hr("TEST 6 — Bad action string  (expect ValueError)")
    reset("u6")
    try:
        run_execution("u6", "AAPL", "HOLD", 10, price_override=190.23)
        print("  ✗  Should have raised ValueError!")
        sys.exit(1)
    except ValueError as e:
        print(f"  ✓  Correctly rejected: {e}")


# ─── Runner ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n🚀  Sentinel Execution Agent — Smoke Test Suite")

    test_buy_success()
    test_sell_success()
    test_insufficient_funds()
    test_insufficient_shares()
    test_sell_no_position()
    test_invalid_action()

    print(f"\n{'═'*55}")
    print("  ✅  All 6 tests passed.")
    print(f"{'═'*55}\n")
