from typing import Dict, Any, List
from app.services.policy_service import enforce_constraints

def validate_intent(trade: Dict[str, Any], avoid_sectors: List[str], context: Dict[str, Any] = None) -> Dict[str, Any]:
    """Agent for guarding and validating intent execution safely before clearing."""
    context = context or {}
    
    sector = trade.get("sector", "").lower()
    avoid_sectors_lower = [s.lower() for s in avoid_sectors]
    
    if sector in avoid_sectors_lower:
        return {
            "status": "BLOCKED",
            "decision": "Trade Blocked by Guard Component",
            "violations": [f"Trade violates ESG constraint: {sector} sector not allowed"],
            "modifications": []
        }
        
    return enforce_constraints(trade, avoid_sectors, context)
