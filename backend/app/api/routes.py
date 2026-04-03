import logging
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

from app.models.request_models import (
    AnalyzeRequest, PortfolioRequest, SimulateRequest,
    ValidateTradeRequest, ExecuteTradeRequest, ExplainRequest,
    ClimateScoresRequest, PoliciesRequest
)
from app.models.response_models import HealthResponse, AnalyzeResponse

# Import Agents
from app.agents.master import run_pipeline
from app.agents.climate import analyze_climate_impact
from app.agents.portfolio import optimize_portfolio
from app.agents.simulation import simulate_scenario
from app.agents.guard import validate_intent
from app.agents.trader import execute_trade
from app.agents.explain import generate_explanation

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint to verify API is active."""
    try:
        return HealthResponse(status="success", message="Sentinel API is healthy")
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/analyze", response_model=Dict[str, Any])
def analyze(request: AnalyzeRequest) -> Dict[str, Any]:
    """Run the entire autonomous investing orchestration pipeline."""
    try:
        logger.info(f"Triggering Master Pipeline for budget: {request.budget}")
        input_data = {
            "budget": request.budget,
            "risk_level": request.risk_level,
            "max_trade": request.max_trade,
            "avoid_sectors": request.avoid_sectors
        }
        result = run_pipeline(input_data)
        return result
    except Exception as e:
        logger.error(f"Error analyzing pipeline: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/portfolio")
def portfolio(request: PortfolioRequest) -> Dict[str, Any]:
    """Process and optimize a portfolio using the standalone Agent."""
    try:
        logger.info("Triggering distinct Portfolio Agent mapping")
        # Needs mocked climate and financial data if calling independently
        mock_climate = analyze_climate_impact([])
        mock_financial = {"market_sentiment": "moderate", "expected_return": 0.08, "volatility": 0.10}
        
        return optimize_portfolio(request.budget, mock_climate, mock_financial)
    except Exception as e:
        logger.error(f"Error processing portfolio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/climate-scores")
def get_climate_scores() -> Dict[str, Any]:
    """Get standalone climate scores via the proxy agent."""
    try:
        logger.info("Triggering Climate Agent manually")
        # Fetch generic climate scores with no avoid filters
        return analyze_climate_impact([])
    except Exception as e:
        logger.error(f"Error fetching climate scores: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/simulate")
def simulate(request: SimulateRequest) -> Dict[str, Any]:
    """Run a scenario simulation independently."""
    try:
        logger.info("Triggering Simulation Agent manually")
        budget = request.parameters.get("budget", 10000.0) if request.parameters else 10000.0
        # Convert portfolio list into a dict for agent args if needed, or pass list natively
        mock_portfolio = {"holdings": request.portfolio} if request.portfolio else {}
        return simulate_scenario(budget, mock_portfolio)
    except Exception as e:
        logger.error(f"Error running simulation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/validate-trade")
def validate_trade(request: ValidateTradeRequest) -> Dict[str, Any]:
    """Manually test the intent Guard Agent against an arbitrary trade payload."""
    try:
        logger.info("Triggering Guard Agent manually")
        guard_context = {
            "max_trade_size": 50000.0,
            "max_risk_threshold": 80,
            "max_allocation_pct": 0.20,
            "portfolio_value": 100000.0
        }
        return validate_intent(request.trade, [], guard_context)
    except Exception as e:
        logger.error(f"Error validating trade: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/policies")
def get_policies() -> Dict[str, Any]:
    """Retrieve active compliance/climate policies dictating Guard rules."""
    try:
        logger.info("Fetching static Guard policies")
        return {
            "active_policies": [
                {"id": "intent_01", "name": "Sector Avoidance", "description": "Blocks execution if asset matches user avoid_list."},
                {"id": "risk_01", "name": "Max Drawdown Cap", "description": "Blocks if simulation predicts drawdown > user tolerance."},
                {"id": "alloc_01", "name": "Allocation Constraint", "description": "Prohibits any single asset from breaching 20% of net liquidity."}
            ]
        }
    except Exception as e:
        logger.error(f"Error fetching policies: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/execute-trade")
def execute_trade_endpoint(request: ExecuteTradeRequest) -> Dict[str, Any]:
    """Force an execution directly to Alpaca paper systems."""
    try:
        logger.info("Triggering Trading Agent manually")
        return execute_trade(request.trade)
    except Exception as e:
        logger.error(f"Error executing trade: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/explain")
def explain(request: ExplainRequest) -> Dict[str, str]:
    """Provide a mocked pipeline state dictionary to receive an overarching string explanation."""
    try:
        logger.info("Triggering Explainer Agent manually")
        explanation = generate_explanation({"guard": {"decision": request.guard_decision or "Unknown", "status": "APPROVED", "modifications": []}})
        return {"explanation": explanation}
    except Exception as e:
        logger.error(f"Error generating explanation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
