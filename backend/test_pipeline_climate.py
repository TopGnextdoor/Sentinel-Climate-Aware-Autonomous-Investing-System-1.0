from app.agents.orchestrator import orchestrate

FOSSIL_TICKERS = {"XOM", "CVX", "BP", "COP", "SLB"}
FOSSIL_SECTORS = {"fossil fuels", "fossil", "oil", "gas", "coal"}

input_data = {
    "budget": 100000,
    "risk_level": "moderate",
    "max_trade": 50000,
    "avoid_sectors": ["fossil fuels"]
}

result = orchestrate(input_data)

climate  = result.get("climate_data", {})
portfolio = result.get("portfolio", {})

green_score      = climate.get("green_score", 0)
eligible_assets  = climate.get("eligible_assets", [])
avoided_sectors  = climate.get("avoided_sectors_applied", [])
holdings         = portfolio.get("holdings", [])

PASS = "[PASS]"
FAIL = "[FAIL]"

# ── 1. ESG-based climate score ─────────────────────────────────
score_ok = green_score > 0
print(f"{PASS if score_ok else FAIL} Climate score based on ESG: {green_score}")

# ── 2. Eligible assets list is non-empty ──────────────────────
assets_ok = len(eligible_assets) > 0
tickers_in_eligible = [a["ticker"] for a in eligible_assets]
print(f"{PASS if assets_ok else FAIL} ESG-filtered assets present: {tickers_in_eligible}")

# ── 3. No fossil sector in eligible assets ────────────────────
fossil_in_eligible = [
    a["ticker"] for a in eligible_assets
    if a.get("sector", "").lower() in FOSSIL_SECTORS
    or a.get("ticker") in FOSSIL_TICKERS
]
no_fossil_eligible = len(fossil_in_eligible) == 0
print(f"{PASS if no_fossil_eligible else FAIL} No fossil stocks in eligible assets "
      f"(found: {fossil_in_eligible or 'none'})")

# ── 4. Portfolio holdings don't contain fossil stocks ─────────
portfolio_tickers = [h.get("ticker") for h in holdings]
fossil_in_portfolio = [t for t in portfolio_tickers if t in FOSSIL_TICKERS]
no_fossil_portfolio = len(fossil_in_portfolio) == 0
print(f"{PASS if no_fossil_portfolio else FAIL} Portfolio MUST NOT include fossil stocks "
      f"(found: {fossil_in_portfolio or 'none'}) → holdings: {portfolio_tickers}")

# ── 5. ESG scores per eligible asset ─────────────────────────
print("\nPer-Asset ESG Scores:")
for a in eligible_assets:
    print(f"  {a['ticker']}: climate_score={a['climate_score']}  sector={a['sector']}  risk={a['risk_level']}")

# ── Summary ───────────────────────────────────────────────────
all_pass = all([score_ok, assets_ok, no_fossil_eligible, no_fossil_portfolio])
print(f"\n{'='*50}")
print(f"RESULT: {'ALL CHECKS PASSED ✅' if all_pass else 'SOME CHECKS FAILED ❌'}")