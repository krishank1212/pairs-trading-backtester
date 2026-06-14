from statsmodels.tsa.stattools import coint

def cointegration_test(data):
    '''
    Perform Engle-Granger cointegration test between SHELL and BP
    Args:
        data (pd.DataFrame): A dataframe with the prices of BP and SHELL
    Returns:
        p_value (float): The p-value of the cointegration test
        is_cointegrated (bool): True if the series are cointegrated, False otherwise
    '''
    stat, p_value, critical_values = coint(data['SHEL'], data['BP'])
    is_cointegrated = p_value < 0.05 
    return p_value, is_cointegrated #