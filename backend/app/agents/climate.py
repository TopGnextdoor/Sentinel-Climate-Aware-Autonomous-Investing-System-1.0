from typing import Dict, Any, List
from app.services.climate_data import fetch_climate_metrics

def analyze_climate_impact(avoid_sectors: List[str], esg_threshold: float = 60.0) -> Dict[str, Any]:
    """Thin wrapper for climate impact analysis using JSON data, filtering by ESG threshold."""
    return fetch_climate_metrics(avoid_sectors, esg_threshold)
