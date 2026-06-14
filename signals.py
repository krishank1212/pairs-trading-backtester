import pandas as pd
def signals(spread, W=60, exit_threshold=0.5, enter_threshold=2):
    '''Generate trading signals based on the spread and the thresholds
    Args:
        spread (pd.Series): A series with the spread between BP and SHELL
        W integer: The rolling window size for calculating the mean and standard deviation of the spread
    Returns:
        pd.Series: A series with the trading signals (1 for long, -1 for short, 0 for no position)
    '''
    mean = spread.rolling(W).mean()
    std = spread.rolling(W).std()
    z_score = (spread - mean) / std
    signals = pd.Series(index=spread.index, data=0)
  
        
    for i in range(1, len(spread)):
        if signals.iloc[i-1] == 0:
            if z_score.iloc[i] > enter_threshold:
                signals.iloc[i] = -1
            elif z_score.iloc[i] < -enter_threshold:
                signals.iloc[i] = 1
        elif signals.iloc[i-1] == 1:
            if abs(z_score.iloc[i]) < exit_threshold:
                signals.iloc[i] = 0
            else:
                signals.iloc[i] = 1
        elif signals.iloc[i-1] == -1:
            if abs(z_score.iloc[i]) < exit_threshold:
                signals.iloc[i] = 0
            else:
                signals.iloc[i] = -1
    return signals, z_score

