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
from app.agents.orchestrator import orchestrate
from app.agents.climate import analyze_climate_impact
from app.agents.portfolio import optimize_portfolio
from app.agents.simulation import simulate_scenario
from app.agents.guard import validate_intent
from app.agents.trader import execute_trade
from app.agents.explain import generate_explanation

# Security & Dependency Injection
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.utils.security import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials", headers={"WWW-Authenticate": "Bearer"})
    user_id = payload.get("sub")
    return user_id

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
def analyze(request: AnalyzeRequest, current_user: str = Depends(get_current_user)) -> Dict[str, Any]:
    """Run the entire autonomous investing orchestration pipeline."""
    try:
        logger.info(f"Triggering Dynamic Orchestrator for budget: {request.budget}")
        input_data = {
            "budget": request.budget,
            "risk_level": request.risk_level,
            "max_trade": request.max_trade,
            "avoid_sectors": request.avoid_sectors
        }
        result = orchestrate(input_data)
        return result
    except Exception as e:
        logger.error(f"Error analyzing pipeline: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/portfolio")
def portfolio(request: PortfolioRequest, current_user: str = Depends(get_current_user)) -> Dict[str, Any]:
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
def execute_trade_endpoint(request: ExecuteTradeRequest, current_user: str = Depends(get_current_user)) -> Dict[str, Any]:
    """Force an execution directly to Alpaca paper systems."""
    try:
        logger.info("Triggering Trading Agent manually")
        return execute_trade(request.trade)
    except Exception as e:
        logger.error(f"Error executing trade: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

from app.services.insights_engine import generate_insights_data

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

@router.post("/insights")
def get_insights(request: PortfolioRequest) -> Dict[str, Any]:
    """Fetch rich dynamic HTML dashboard data for ESG insights."""
    try:
        logger.info("Generating dynamic ESG insights for dashboard")
        return generate_insights_data(request.portfolio)
    except Exception as e:
        logger.error(f"Error generating insights: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────────────────────────────────────
#  MARKET DATA — Real OHLCV via yfinance
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/market-data/{ticker}")
def get_market_data(
    ticker: str,
    period: str = "1y",
    interval: str = "1wk"
) -> Dict[str, Any]:
    """
    Fetch real OHLCV candlestick data for the front-end trading chart.

    Query params:
      period   — 1d | 5d | 1mo | 3mo | 6mo | 1y | 2y | 5y | max
      interval — 1m | 2m | 5m | 15m | 30m | 60m | 90m | 1h | 1d | 5d | 1wk | 1mo | 3mo

    Returns { ticker, period, interval, candles: [{time, open, high, low, close, volume}], info }
    """
    try:
        import yfinance as yf

        ticker = ticker.upper().strip()
        logger.info(f"Fetching real market data via yfinance: {ticker} period={period} interval={interval}")

        stock = yf.Ticker(ticker)
        hist = stock.history(period=period, interval=interval)

        if hist.empty:
            raise HTTPException(status_code=404, detail=f"No data found for ticker '{ticker}'")

        candles = []
        for ts, row in hist.iterrows():
            # Convert pandas Timestamp to Unix epoch (seconds) for Lightweight Charts
            unix_time = int(ts.timestamp())
            candles.append({
                "time":   unix_time,
                "open":   round(float(row["Open"]),   2),
                "high":   round(float(row["High"]),   2),
                "low":    round(float(row["Low"]),    2),
                "close":  round(float(row["Close"]),  2),
                "volume": int(row["Volume"]),
            })

        # Get current info for the stats bar (best-effort)
        info = {}
        try:
            raw = stock.fast_info
            info = {
                "regularMarketPrice":      round(float(raw.get("lastPrice", 0) or 0),        2),
                "regularMarketOpen":       round(float(raw.get("open", 0) or 0),              2),
                "regularMarketDayHigh":    round(float(raw.get("dayHigh", 0) or 0),          2),
                "regularMarketDayLow":     round(float(raw.get("dayLow", 0) or 0),           2),
                "fiftyTwoWeekHigh":        round(float(raw.get("yearHigh", 0) or 0),         2),
                "fiftyTwoWeekLow":         round(float(raw.get("yearLow", 0) or 0),          2),
                "regularMarketVolume":     int(raw.get("lastVolume", 0) or 0),
                "shortName":               ticker,
            }
        except Exception as e:
            logger.warning(f"Could not fetch fast_info for {ticker}: {e}")

        return {
            "ticker":   ticker,
            "period":   period,
            "interval": interval,
            "candles":  candles,
            "info":     info,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching real market data for {ticker}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch market data from yfinance: {str(e)}")

# ── USER AUTHENTICATION (MVP) ──────────────────────────────────
from app.models.user import UserCreate, UserLogin, create_user, get_user_by_email, verify_password
from app.utils.security import create_access_token

@router.post("/signup")
def signup(user_data: UserCreate):
    """Register a new user to the MVP database."""
    try:
        user = create_user(user_data)
        access_token = create_access_token({"sub": user.id, "email": user.email, "username": user.username, "role": user.role})
        return {"message": "User created successfully", "access_token": access_token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(user_data: UserLogin):
    """Secure Login issuing an ephemeral JWT Bearer identity token."""
    user = get_user_by_email(user_data.email)
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
        
    access_token = create_access_token({"sub": user.id, "email": user.email, "username": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}
