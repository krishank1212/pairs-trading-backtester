import pandas as pd
def PnL(data, beta, signals):
    '''Calculate the PnL of the trading strategy
    Args:
        data (pd.DataFrame): A dataframe with the prices of BP and SHELL
        beta: The beta coefficient from the regression of SHELL on BP
        signals (pd.Series): A series with the trading signals (1 for long, -1 for short, 0 for no position)
    Returns:
        pd.Series: A series with the PnL of the trading strategy
    '''
    delta_shel = data['SHEL'].diff()
    delta_bp = data['BP'].diff()
    pnl = signals.shift(1) * (delta_shel - beta * delta_bp)
    return pnl

def backtest(data, beta, signals):
    '''Backtest the trading strategy
    Args:
        data (pd.DataFrame): A dataframe with the prices of BP and SHELL
        beta: The beta coefficient from the regression of SHELL on BP
        signals (pd.Series): A series with the trading signals (1 for long, -1 for short, 0 for no position)
    Returns:
        pd.Series: A series with the cumulative PnL of the trading strategy
    '''
    pnl = PnL(data, beta, signals)
    cumulative_pnl = pnl.cumsum()
    max_drawdown = (pnl.cumsum() - pnl.cumsum().cummax()).min()
    sharpe_ratio = pnl.mean() / pnl.std() * (252 ** 0.5)  # Annualized Sharpe ratio

    return cumulative_pnl, max_drawdown, sharpe_ratio

