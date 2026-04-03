from app.agents.climate import analyze_climate_impact

input_data = {
    "avoid_sectors": ["fossil"]
}

# Set threshold lower than 55 so TSLA is included in the eligible assets
result = analyze_climate_impact(input_data.get("avoid_sectors", []), esg_threshold=50.0)

print({
    "green_score": result.get("green_score"),
    "eligible_assets": [a["ticker"] for a in result.get("eligible_assets", [])]
})