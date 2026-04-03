from app.services.climate_data import get_esg_score

tickers = ["AAPL", "MSFT", "TSLA"]

for t in tickers:
    score = get_esg_score(t)
    print(f"{t}: {score}")

print(get_esg_score("RANDOM123"))