from app.services.market_data import get_stock_price, get_multiple_prices

# Test single stock
print(get_stock_price("INVALID123"))

# Test multiple stocks
prices = get_multiple_prices(["AAPL", "MSFT", "TSLA"])
print("Multiple Prices:", prices)