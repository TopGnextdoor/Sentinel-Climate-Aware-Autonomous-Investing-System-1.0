from typing import Dict, Any

from app.agents.climate import analyze_climate_impact
from app.agents.financial import analyze_market_trends
from app.agents.simulation import simulate_scenario
from app.agents.portfolio import optimize_portfolio
from app.agents.trader import generate_trade_proposals, execute_trade
from app.agents.guard import validate_intent
from app.agents.explain import generate_explanation

def orchestrate(input_data: dict) -> dict:
    """
    Dynamic Orchestrator
    Executes agents step-by-step with dynamic conditions.
    """
    orchestration_steps = []
    
    # Extract input data with defaults
    avoid_sectors = input_data.get("avoid_sectors", [])
    risk_level = input_data.get("risk_level", "medium")
    budget = input_data.get("budget", 10000.0)
    max_trade = input_data.get("max_trade", 5000.0)
    
    # 1. Climate
    climate_scores = analyze_climate_impact(avoid_sectors)
    orchestration_steps.append({"agent": "climate", "status": "completed"})
    
    # 2. Financial
    financial_data = analyze_market_trends(risk_level)
    orchestration_steps.append({"agent": "financial", "status": "completed"})
    
    # 3. Simulation (conditional)
    simulation = None
    if risk_level.lower() == "high":
        # Portfolio isn't generated yet based on required order, so pass empty dict
        simulation = simulate_scenario(budget, {})
        orchestration_steps.append({"agent": "simulation", "status": "completed"})
    else:
        orchestration_steps.append({"agent": "simulation", "status": "skipped"})
        
    # 4. Portfolio
    portfolio = optimize_portfolio(budget, climate_scores, financial_data)
    orchestration_steps.append({"agent": "portfolio", "status": "completed"})
    
    # 5. Trade
    trade = generate_trade_proposals(portfolio, max_trade)
    orchestration_steps.append({"agent": "trade", "status": "completed"})
    
    # 6. Guard
    guard_context = {
        "max_trade_size": max_trade,
        "max_risk_threshold": 80 if risk_level.lower() != "high" else 95,
        "max_allocation_pct": 0.20,
        "portfolio_value": portfolio.get("invested_amount", 0) + portfolio.get("cash_balance", 10000.0)
    }
    
    proposed_trade = trade.get("proposed_trade", {})
    guard = validate_intent(proposed_trade, avoid_sectors, guard_context)
    orchestration_steps.append({"agent": "guard", "status": "completed"})
    
    # 7. Trader (conditional)
    execution = None
    guard_status = guard.get("status")
    
    if guard_status == "APPROVED":
        final_trade = guard.get("adjusted_trade") or guard.get("original_trade", proposed_trade)
        execution = execute_trade(final_trade)
        orchestration_steps.append({"agent": "trader", "status": "completed"})
    else:
        status_value = "blocked" if guard_status == "BLOCKED" else "skipped"
        orchestration_steps.append({"agent": "trader", "status": status_value})
        
    # 8. Explain
    # Create the state expected by existing generate_explanation
    pipeline_state = {
        "climate_data": climate_scores,
        "guard": guard,
        "simulation": simulation or {},
    }
    explanation = generate_explanation(pipeline_state)
    orchestration_steps.append({"agent": "explain", "status": "completed"})
    
    return {
        "portfolio": portfolio,
        "climate_data": climate_scores,
        "financial_data": financial_data,
        "simulation": simulation,
        "trade": trade,
        "guard": guard,
        "execution": execution,
        "explanation": explanation,
        "orchestration": orchestration_steps
    }
