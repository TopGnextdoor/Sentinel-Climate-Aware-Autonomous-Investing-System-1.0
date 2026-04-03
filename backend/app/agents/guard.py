from typing import Dict, Any, List
from app.services.policy_service import enforce_constraints

def validate_intent(trade: Dict[str, Any], avoid_sectors: List[str], context: Dict[str, Any] = None) -> Dict[str, Any]:
    """Agent for guarding and validating intent execution safely before clearing."""
    context = context or {}
    return enforce_constraints(trade, avoid_sectors, context)
