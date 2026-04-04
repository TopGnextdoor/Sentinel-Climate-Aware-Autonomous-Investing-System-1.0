"""
Sentinel — Execution Agent
Simulates trade execution using real-time stock prices.

Responsibilities:
  - Fetch the current market price via market_data service
  - Calculate total cost / proceeds
  - Validate funds (BUY) or share availability (SELL)
  - Delegate the actual portfolio mutation to the portfolio model layer
  - Return a structured execution receipt

Usage:
    from app.agents.execution import run_execution

    result = run_execution(
        user_id="user_123",
        ticker="AAPL",
        action="BUY",      # or "SELL"
        quantity=100,
    )
"""

from typing import Any, Dict, Optional
from datetime import datetime, timezone

from app.services.market_data import get_stock_price
from app.models.portfolio import (
    execute_buy,
    execute_sell,
    get_or_create_portfolio,
    get_portfolio_summary,
)


# ─── Public API ───────────────────────────────────────────────────────────────

def run_execution(
    user_id: str,
    ticker: str,
    action: str,
    quantity: float,
    price_override: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Execute a paper trade for *user_id*.

    Args:
        user_id:        Authenticated user's identifier.
        ticker:         Stock symbol, e.g. "AAPL".
        action:         "BUY" or "SELL" (case-insensitive).
        quantity:       Number of shares to trade (must be > 0).
        price_override: Optional fixed price; skips live fetch when provided
                        (useful for back-tests and unit tests).

    Returns:
        Dict with keys:
            status       – "EXECUTED" on success
            action       – "BUY" or "SELL"
            ticker       – normalised ticker symbol
            quantity     – shares traded
            price        – per-share price used
            total_cost   – total $ amount of the trade
            trade_id     – unique ID for this trade record
            timestamp    – ISO-8601 UTC execution time
            portfolio    – snapshot of updated portfolio summary

    Raises:
        ValueError: On invalid inputs, insufficient cash (BUY),
                    or insufficient shares (SELL).
    """

    # ── 1. Normalise & validate inputs ────────────────────────────────────────
    ticker   = str(ticker).upper().strip()
    action   = str(action).upper().strip()
    quantity = float(quantity)

    if not ticker:
        raise ValueError("Execution requires a non-empty ticker symbol.")
    if quantity <= 0:
        raise ValueError(f"Quantity must be positive, got {quantity}.")
    if action not in ("BUY", "SELL"):
        raise ValueError(f"Action must be 'BUY' or 'SELL', got '{action}'.")

    # ── 2. Fetch live market price ─────────────────────────────────────────────
    price = price_override if price_override is not None else get_stock_price(ticker)

    if price <= 0:
        raise ValueError(
            f"Unable to obtain a valid price for '{ticker}' "
            f"(received {price}). Trade aborted."
        )

    # ── 3. Calculate total cost / proceeds ────────────────────────────────────
    total_cost = round(price * quantity, 2)

    # ── 4. Pre-flight checks (fast-fail with informative messages) ────────────
    portfolio = get_or_create_portfolio(user_id)

    if action == "BUY":
        _validate_buy(portfolio, total_cost)
    else:
        _validate_sell(portfolio, ticker, quantity)

    # ── 5. Execute via portfolio model layer ──────────────────────────────────
    if action == "BUY":
        record = execute_buy(user_id, ticker, quantity, price)
    else:
        record = execute_sell(user_id, ticker, quantity, price)

    # ── 6. Build & return execution receipt ───────────────────────────────────
    summary = get_portfolio_summary(user_id)

    return {
        "status":     "EXECUTED",
        "action":     action,
        "ticker":     ticker,
        "quantity":   quantity,
        "price":      round(price, 2),
        "total_cost": total_cost,
        "trade_id":   record.trade_id,
        "timestamp":  record.timestamp,
        "portfolio":  summary.model_dump(),
    }


# ─── Internal Validators ──────────────────────────────────────────────────────

def _validate_buy(portfolio, total_cost: float) -> None:
    """Raise ValueError if the user cannot afford the purchase."""
    if total_cost > portfolio.cash_balance:
        raise ValueError(
            f"Insufficient funds. "
            f"Required: ${total_cost:,.2f} | "
            f"Available: ${portfolio.cash_balance:,.2f}"
        )


def _validate_sell(portfolio, ticker: str, quantity: float) -> None:
    """Raise ValueError if the user does not hold enough shares to sell."""
    holding = portfolio.holdings.get(ticker)
    if holding is None:
        raise ValueError(
            f"No position found for '{ticker}'. Cannot sell shares you don't own."
        )
    if quantity > holding.quantity:
        raise ValueError(
            f"Insufficient shares for '{ticker}'. "
            f"Attempting to sell {quantity} | "
            f"Held: {holding.quantity}"
        )


# ─── Convenience Wrappers ─────────────────────────────────────────────────────

def execute_buy_order(
    user_id: str,
    ticker: str,
    quantity: float,
    price_override: Optional[float] = None,
) -> Dict[str, Any]:
    """Shorthand for a BUY execution."""
    return run_execution(user_id, ticker, "BUY", quantity, price_override)


def execute_sell_order(
    user_id: str,
    ticker: str,
    quantity: float,
    price_override: Optional[float] = None,
) -> Dict[str, Any]:
    """Shorthand for a SELL execution."""
    return run_execution(user_id, ticker, "SELL", quantity, price_override)
