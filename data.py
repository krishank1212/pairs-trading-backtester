import yfinance as yf
def get_prices():
    '''Get the prices of BP and SHELL from Yahoo Finance from 2000-01-01 to today
    Returns:
        pd.DataFrame: A dataframe with the prices of BP and SHELL
    '''
    data = yf.download(['BP.L', 'SHEL.L'], '2000-01-01')
    data = data.xs('Close', axis=1, level=0)
    data.dropna(inplace=True)
    data.rename(inplace=True, columns={"BP.L" : "BP", "SHEL.L" : "SHEL"})
    return data


