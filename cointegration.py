from statsmodels.tsa.stattools import adfuller
def cointegration_test(resids):
    '''Perform the Augmented Dickey-Fuller test on the residuals to check for cointegration
    Args:
        resids (pd.Series): A series with the residuals from the regression of SHELL on BP
    Returns:
        float: The p-value from the ADF test
    '''
    adf_result = adfuller(resids)
    is_cointegrated = adf_result[1] < 0.05  # Check if p-value is less than 0.05
    return adf_result[1], is_cointegrated  # Return the p-value, and whether the series is cointegrated