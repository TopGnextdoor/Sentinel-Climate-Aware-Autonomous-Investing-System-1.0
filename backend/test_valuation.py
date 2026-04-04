import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app.services.portfolio_service import get_portfolio_value, get_performance_summary
from app.models.portfolio import _portfolio_store, Portfolio, execute_buy

# seed a test portfolio with one trade
uid = 'val_test_2'
_portfolio_store[uid] = Portfolio(user_id=uid, cash_balance=80_000.0)

# execute a buy
rec = execute_buy(uid, 'AAPL', 10, 190.23)

val = get_portfolio_value(uid)
perf = get_performance_summary(uid)

assert val['total_value'] > 0, "total_value should be > 0"
assert val['cash'] == round(80_000 - 1902.3, 2), "Cash incorrect"
assert val['holdings_value'] > 0, "holdings_value should be > 0"

assert perf['total_value'] == val['total_value'], "perf and val total mismatch"
assert perf['trade_count'] == 1, "trade count should be 1"
assert perf['buy_count'] == 1, "buy count should be 1"
assert perf['best_performer'] is not None, "best performer should be present"
assert perf['overall_pnl'] is not None, "pnl should be present"
assert 'win_rate_pct' in perf, "win_rate_pct should be present"

print('portfolio/value  :', val)
print()
print('portfolio/performance (summary):')
for k,v in perf.items():
    if k != 'holdings':
        print(f'  {k}: {v}')
print('  holdings:', perf['holdings'])
print()
print('All assertions PASSED!')
