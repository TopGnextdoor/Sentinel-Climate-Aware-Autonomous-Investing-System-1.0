from typing import Dict, Any, List
from app.services.climate_data import fetch_climate_metrics

def analyze_climate_impact(avoid_sectors: List[str]) -> Dict[str, Any]:
    """Thin wrapper for climate impact analysis using JSON data."""
    return fetch_climate_metrics(avoid_sectors)
