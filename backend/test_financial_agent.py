from app.services.risk import calculate_market_trends

result = calculate_market_trends("moderate")

print("=" * 55)
print("FINANCIAL ANALYSIS — REAL MARKET SIGNALS")
print("=" * 55)
print(f"  Overall Sentiment : {result['market_sentiment'].upper()}")
print(f"  Sentiment Label   : {result['sentiment_label']}")
print(f"  Expected Return   : {result['expected_return']}")
print(f"  Volatility        : {result['volatility']}")
print(f"  Market Risk Score : {result['market_risk_score']}")

print("\nPer-Ticker Breakdown:")
for s in result.get("per_ticker_signals", []):
    print(f"  {s['ticker']:6} | return={s['daily_return_pct']:>7.4f}%"
          f"  vol={s['volatility_pct']:>6.4f}%"
          f"  {s['sentiment'].upper():8} | {s['sentiment_label']}")

print("\nVALIDATION:")
PASS = "[PASS]"
FAIL = "[FAIL]"
print(f"  {PASS if result['market_sentiment'] in ('bullish','bearish','neutral') else FAIL} Sentiment label is valid")
print(f"  {PASS if result['expected_return'] != 0.08 else FAIL} Expected return is not the old hardcoded dummy")
print(f"  {PASS if len(result.get('per_ticker_signals', [])) > 0 else FAIL} Per-ticker signals present")
print(f"  {PASS if result['volatility'] >= 0 else FAIL} Volatility is non-negative")
print("=" * 55)
