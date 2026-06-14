from data import get_prices
from spread import get_spread
from signals import signals
from backtest import backtest
from cointegration import cointegration_test
import matplotlib.pyplot as plt

prices = get_prices()
spread, beta = get_spread(prices)
results = cointegration_test(prices)
print(f"p-value: {results[0]}, Cointegrated: {results[1]}")
sig, z_score = signals(spread)
cumulative_pnl, max_drawdown, sharpe_ratio = backtest(prices, beta, sig)
print(f"Cumulative PnL: {cumulative_pnl.iloc[-1]}")
print(f"Max Drawdown: {max_drawdown}")
print(f"Sharpe Ratio: {sharpe_ratio}")


# Plot the cumulative PnL
plt.figure(figsize=(12, 6))
plt.plot(cumulative_pnl, label='Cumulative PnL')
plt.title('Cumulative PnL of the Trading Strategy')
plt.xlabel('Date')
plt.ylabel('Cumulative PnL')
plt.legend()
plt.grid()
plt.show()

# Plot the spread
plt.figure(figsize=(12, 6))
plt.plot(spread, label='Spread (SHELL - beta * BP)')
plt.title('Spread between SHELL and BP')
plt.xlabel('Date')
plt.ylabel('Spread')
plt.legend()
plt.grid()
plt.show()

# Plot of z-score of the spread
plt.figure(figsize=(12, 6))
plt.plot(z_score, label='Z-score of Spread')
plt.axhline(2, color='red', linestyle='--', label='Short Entry Threshold')
plt.axhline(-2, color='green', linestyle='--', label='Long Entry Threshold')
plt.axhline(0.5, color='orange', linestyle='--', label='Exit Threshold')
plt.axhline(-0.5, color='orange', linestyle='--', label='Exit Threshold')
plt.title('Z-score of the Spread between SHELL and BP')
plt.xlabel('Date')
plt.ylabel('Z-score')
plt.legend()
plt.grid()
plt.show()


#Sub-period analysis
'''
Analyses the performance of the trading strategy between 3 sub-periods: 
2000-2008, 2008-2020, 2020-present. 
It calculates the cumulative PnL, max drawdown, and Sharpe ratio for each 
sub-period and plots the cumulative PnL for each sub-period.
'''
subperiods = {
    '2005-2010': prices.loc['2005-01-01':'2009-12-31'],
    '2010-2020': prices.loc['2010-01-01':'2019-12-31'],
    '2020-present': prices.loc['2020-01-01':]
}

for name, data in subperiods.items():
    spread, beta = get_spread(data)
    sig, z_score = signals(spread)
    results = cointegration_test(data)
    print(f"Sub-period: {name}, p-value: {results[0]}, Cointegrated: {results[1]}")
    cumulative_pnl, max_drawdown, sharpe_ratio = backtest(data, beta, sig)
    print(f"Sub-period: {name}")
    print(f"Cumulative PnL: {cumulative_pnl.iloc[-1]}")
    print(f"Max Drawdown: {max_drawdown}")
    print(f"Sharpe Ratio: {sharpe_ratio}")

    # Plot the cumulative PnL for each sub-period
    plt.figure(figsize=(12, 6))
    plt.plot(cumulative_pnl, label=f'Cumulative PnL ({name})')
    plt.title(f'Cumulative PnL of the Trading Strategy ({name})')
    plt.xlabel('Date')
    plt.ylabel('Cumulative PnL')
    plt.legend()
    plt.grid()
    plt.show()