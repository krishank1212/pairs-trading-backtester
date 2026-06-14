import statsmodels.api

def get_spread(data):
    '''Get the spread between BP and SHELL
    Args:
        data (pd.DataFrame): A dataframe with the prices of BP and SHELL
    Returns:
        pd.Series: A series with the spread between BP and SHELL
        beta: The beta coefficient from the regression of SHELL on BP
    '''
    bp_with_const = statsmodels.api.add_constant(data['BP'])
    model = statsmodels.api.OLS(data['SHEL'], bp_with_const)
    results = model.fit()
    spread = results.resid
    beta = results.params.iloc[1]
    return spread, beta