import logging
from typing import Any, Dict, Optional

from app.agents.climate import analyze_climate_impact
from app.agents.financial import analyze_market_trends
from app.agents.simulation import simulate_scenario
from app.agents.portfolio import optimize_portfolio
from app.agents.trader import generate_trade_proposals
from app.agents.guard import validate_intent
from app.agents.explain import generate_explanation
from app.agents.execution import run_execution

logger = logging.getLogger(__name__)

def orchestrate(input_data: dict, user_id: Optional[str] = None) -> dict:
    """
    Dynamic Orchestrator — all agents use real data.
    Flow: Climate → Financial → Simulation → Portfolio → Trade →
          Guard → Execution → Explain

    Args:
        input_data: Pipeline inputs (budget, risk_level, etc.).
        user_id:    Authenticated user whose paper portfolio is updated.
                    Defaults to a shared 'system' account when called
                    from the /analyze endpoint without a user context.
    """
    _user_id = user_id or "system"
    orchestration_steps = []

    # ── Extract inputs ────────────────────────────────────────
    avoid_sectors  = input_data.get("avoid_sectors", [])
    risk_level     = input_data.get("risk_level", "moderate")
    budget         = input_data.get("budget", 10000.0)
    max_trade      = input_data.get("max_trade", 5000.0)
    esg_threshold  = float(input_data.get("esg_threshold", 60.0))

    # ── 1. Climate Agent — real ESG scores + sector filter ────
    climate_scores = analyze_climate_impact(avoid_sectors, esg_threshold=esg_threshold)
    eligible_assets = climate_scores.get("eligible_assets", [])
    eligible_tickers = [a["ticker"] for a in eligible_assets]
    orchestration_steps.append({
        "agent": "climate",
        "status": "completed",
        "data_source": "yfinance ESG + static fallback",
        "eligible_tickers": eligible_tickers,
        "green_score": climate_scores.get("green_score"),
    })

    # ── 2. Financial Agent — real price trends + sentiment ────
    # Use the ESG-eligible tickers so financial signals match the portfolio universe
    financial_data = analyze_market_trends(risk_level, tickers=eligible_tickers or None)
    orchestration_steps.append({
        "agent": "financial",
        "status": "completed",
        "data_source": "yfinance 5-day price history",
        "sentiment": financial_data.get("market_sentiment"),
        "sentiment_label": financial_data.get("sentiment_label"),
    })

    # ── 3. Simulation Agent ───────────────────────────────────
    simulation = simulate_scenario(budget, {})
    orchestration_steps.append({"agent": "simulation", "status": "completed"})

    # ── 4. Portfolio Agent — real market prices ───────────────
    portfolio = optimize_portfolio(budget, climate_scores, financial_data)
    orchestration_steps.append({
        "agent": "portfolio",
        "status": "completed",
        "data_source": "yfinance real-time prices",
    })

    # ── 5. Trade Proposal ─────────────────────────────────────
    allowed_assets = [h.get("ticker", "AAPL") for h in portfolio.get("holdings", [])]
    trade = generate_trade_proposals(allowed_assets, max_trade)
    orchestration_steps.append({"agent": "trade", "status": "completed"})

    proposed_trade = trade.get("proposed_trade", {})
    ticker = proposed_trade.get("ticker", "")

    execution_result: Dict[str, Any] = {"status": "SKIPPED", "reason": "Not yet evaluated"}

    if ticker not in allowed_assets:
        trade = {
            "status": "INVALID",
            "reason": "Asset not allowed by ESG constraints",
        }
        guard = {
            "status": "BLOCKED",
            "decision": "Safety Layer Rejection",
            "violations": ["Asset not in allowed universe"],
        }
        execution_result = {
            "status": "SKIPPED",
            "reason": "Guard blocked trade — asset outside ESG-approved universe",
        }
        orchestration_steps.append({"agent": "guard",     "status": "skipped"})
        orchestration_steps.append({"agent": "trader",    "status": "skipped"})
        orchestration_steps.append({"agent": "execution", "status": "skipped"})
    else:
        # ── 6. Guard ─────────────────────────────────────────
        guard_context = {
            "max_trade_size":     max_trade,
            "max_risk_threshold": 80 if risk_level.lower() != "high" else 95,
            "max_allocation_pct": 0.20,
            "portfolio_value":    portfolio.get("invested_amount", 0)
                                  + portfolio.get("cash_balance", 10000.0),
        }
        guard = validate_intent(proposed_trade, avoid_sectors, guard_context)
        guard_status = guard.get("status", "BLOCKED")
        orchestration_steps.append({"agent": "guard", "status": "completed", "decision": guard_status})

        # ── 7. Execution (conditional on Guard APPROVAL) ──────
        if guard_status == "APPROVED":
            final_trade = guard.get("adjusted_trade") or guard.get("original_trade", proposed_trade)
            exec_ticker   = final_trade.get("ticker", ticker)
            exec_quantity = float(final_trade.get("quantity", proposed_trade.get("quantity", 1)))
            exec_price    = final_trade.get("price")  # use guard-approved price if present

            try:
                logger.info(
                    f"[Orchestrator] Execution: {_user_id} BUY "
                    f"{exec_quantity}×{exec_ticker}"
                )
                execution_result = run_execution(
                    user_id=_user_id,
                    ticker=exec_ticker,
                    action="BUY",          # trades proposed by Trader are always BUY
                    quantity=exec_quantity,
                    price_override=exec_price,   # None → live fetch
                )
                orchestration_steps.append({
                    "agent":   "execution",
                    "status":  "completed",
                    "ticker":  exec_ticker,
                    "price":   execution_result.get("price"),
                    "total_cost": execution_result.get("total_cost"),
                })
            except ValueError as exc:
                logger.warning(f"[Orchestrator] Execution rejected: {exc}")
                execution_result = {
                    "status": "REJECTED",
                    "reason": str(exc),
                }
                orchestration_steps.append({
                    "agent":  "execution",
                    "status": "rejected",
                    "reason": str(exc),
                })
        else:
            block_reason = "; ".join(guard.get("violations", [])) or "Guard decision: not approved"
            execution_result = {
                "status": "SKIPPED",
                "reason": f"Guard {guard_status} — {block_reason}",
            }
            orchestration_steps.append({
                "agent":  "execution",
                "status": "skipped",
                "reason": block_reason,
            })

    # ── 8. Explain ────────────────────────────────────────────
    pipeline_state = {
        "climate_data": climate_scores,
        "guard":        guard,
        "simulation":   simulation or {},
    }
    explanation = generate_explanation(pipeline_state)
    orchestration_steps.append({"agent": "explain", "status": "completed"})

    # ── Response ──────────────────────────────────────────────
    return {
        "portfolio":         portfolio,
        "climate_data":      climate_scores,
        "financial_data":    financial_data,
        "simulation":        simulation,
        "trade":             trade,
        "guard":             guard,
        "execution_result":  execution_result,   # NEW — replaces bare 'execution'
        "explanation":       explanation,
        "orchestration":     orchestration_steps,
    }

