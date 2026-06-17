# About the project

This project implements and evaluates a statistical pairs trading strategy applied to BP (BP.L) and Shell (SHEL.L), two major UK-listed oil companies with closely linked economic exposures. The primary aim was not to produce a profitable trading strategy, but to rigorously test whether the pair satisfies the statistical conditions required for pairs trading, investigate how that relationship has evolved across market regimes, and understand the gap between theoretical cointegration and empirical trading performance.

In particular, I test for cointegration across three distinct sub-periods, construct a z-score-based mean-reversion signal, and evaluate strategy performance using Sharpe ratio, cumulative PnL, and maximum drawdown: all with strict causal implementation to avoid look-ahead bias throughout.

The data used for this project was daily closing prices for BP.L and SHEL.L retrieved from Yahoo Finance via `yfinance`, covering approximately 5,400 trading days from January 2005 to June 2026. The start date was chosen to avoid data quality issues with Shell's LSE listing prior to the 2005 Anglo-Dutch merger restructuring.

---

# Mathematical framework

## Cointegration and stationarity

Two price series $P_t^A$ and $P_t^B$ are said to be cointegrated if there exists a linear combination

$$\varepsilon_t = P_t^A - \alpha - \beta P_t^B$$

that is stationary, meaning it has a constant mean, constant variance, and autocovariance that depends only on lag, not on time. Stationarity is the key property that gives a pairs trading strategy its theoretical foundation: a stationary spread has a tendency to revert to its long-run mean, allowing systematic entry and exit signals to be constructed.

Stock prices individually are non-stationary; they exhibit unit root behaviour, meaning shocks accumulate indefinitely with no restoring force. Cointegration identifies pairs where a specific linear combination of two non-stationary series is itself stationary.

## OLS regression and spread construction

The hedge ratio $\beta$ is estimated via ordinary least squares regression of Shell prices on BP prices:

$$P_t^{\text{SHEL}} = \alpha + \beta P_t^{\text{BP}} + \varepsilon_t$$

with $\beta = \mathrm{Cov}(P^{\text{SHEL}}, P^{\text{BP}}) / \mathrm{Var}(P^{\text{BP}})$. The residual series $\varepsilon_t$ is the estimated spread, representing the component of Shell's price unexplained by BP's price.

## Cointegration testing

To test whether $\varepsilon_t$ is stationary, I apply the Engle-Granger two-step procedure via `statsmodels.tsa.stattools.coint`, which uses MacKinnon critical values specifically calibrated for cointegration testing. The null hypothesis is the presence of a unit root (non-stationarity); rejection at the 5% significance level is taken as evidence of cointegration.

Standard Augmented Dickey-Fuller critical values are inappropriate here because the spread is not directly observed; it is estimated from a regression, and this estimation step requires more conservative critical values.

## Trading signal

The spread is standardised using a rolling window of $W = 60$ trading days to produce a z-score:

$$z_t = \frac{\varepsilon_t - \mu_t^{(W)}}{\sigma_t^{(W)}}$$

where $\mu_t^{(W)}$ and $\sigma_t^{(W)}$ are the rolling mean and standard deviation computed over days $[t-W, t-1]$, strictly excluding day $t$ to eliminate look-ahead bias.

Trading signals are generated as follows:

- $z_t > +2$: short Shell, long BP (signal $= -1$)
- $z_t < -2$: long Shell, short BP (signal $= +1$)
- $|z_t| < 0.5$: close position (signal $= 0$)

Positions persist between entry and exit: the signal on day $t$ depends on the signal on day $t-1$, requiring sequential rather than vectorised computation.
<img width="1196" height="597" alt="image" src="https://github.com/user-attachments/assets/d6f34b4b-4807-4ce9-9a53-55173c49f5dd" />

## PnL and performance metrics

Daily PnL is computed as:

$$\text{PnL}_t = \text{signal}_{t-1} \times (\Delta P_t^{\text{SHEL}} - \beta \cdot \Delta P_t^{\text{BP}})$$

using the prior day's signal to avoid look-ahead bias. Performance is assessed using three metrics:

- **Sharpe ratio**: $\frac{\mu_{\text{PnL}}}{\sigma_{\text{PnL}}} \times \sqrt{252}$, annualised assuming 252 trading days
- **Cumulative PnL**: total accumulated profit and loss over the period
- **Maximum drawdown**: the largest peak-to-trough decline in the cumulative PnL series

---

# Implementation

The project is implemented in Python across six modules:

- `data.py`: downloads and cleans BP and Shell closing prices via `yfinance`
- `spread.py`: estimates $\hat{\alpha}$ and $\hat{\beta}$ via OLS and constructs the residual spread
- `cointegration.py`: applies the Engle-Granger test and returns the p-value and a pass/fail boolean
- `signals.py`: computes the rolling z-score and generates entry/exit signals via sequential loop
- `backtest.py`: computes daily PnL, cumulative PnL, Sharpe ratio, and maximum drawdown
- `main.py`: ties the pipeline together and produces all plots and sub-period analysis

---

# Experimental setup

All simulations were performed with the following parameters:

- Rolling window: $W = 60$ trading days
- Entry threshold: $|z_t| > 2$
- Exit threshold: $|z_t| < 0.5$
- Data: BP.L and SHEL.L daily closing prices, January 2005 to June 2026

Sub-period analysis was conducted across three regimes:

| Sub-period | Dates | Motivation |
|---|---|---|
| Pre-Deepwater Horizon | 2005–2010 | Baseline period; both companies operating normally |
| Post-Deepwater Horizon | 2010–2020 | BP's idiosyncratic shock and subsequent recovery |
| Post-pandemic | 2020–present | Structural divergence in corporate strategy |

---

# Quantitative results

## Cointegration test results

| Sub-period | p-value | Cointegrated |
|---|---|---|
| 2005–2010 | 0.230 | No |
| 2010–2020 | 0.011 | Yes |
| 2020–present | 0.555 | No |
| Full period (2005–2026) | 0.783 | No |

## Trading performance by sub-period

| Sub-period | Cumulative PnL | Max Drawdown | Sharpe Ratio |
|---|---|---|---|
| 2005–2010 | 225.8 | -443.7 | 0.206 |
| 2010–2020 | 353.3 | -691.3 | 0.164 |
| 2020–present | 538.7 | -566.1 | 0.309 |
| Full period | 2392.5 | -1002.7 | 0.427 |

<img width="1196" height="597" alt="image" src="https://github.com/user-attachments/assets/1561d371-fd95-4b68-b7c2-b131c656dc89" />
<img width="1196" height="597" alt="image" src="https://github.com/user-attachments/assets/2b396d6f-8bf7-4afb-a505-21c7574e3fef" />
<img width="1196" height="597" alt="image" src="https://github.com/user-attachments/assets/94d4cbb5-a560-4c48-81fc-bd0effce1650" />

---

# Analysis

## Regime-dependent cointegration

The full-period cointegration test (p = 0.783) fails decisively, but this masks important sub-period variation. The 2010–2020 period passes the Engle-Granger test at the 1% significance level (p = 0.011), suggesting the pair was genuinely cointegrated during this regime.

The most plausible explanation is the Deepwater Horizon oil spill in April 2010, which caused BP's share price to collapse by approximately 50% while Shell was largely unaffected. This created a large, persistent dislocation in the spread that slowly reverted over the following decade as BP recovered operationally and financially. The dislocation and its reversion are precisely the conditions that generate a stationary spread (and hence cointegration) over this window.

Pre-2010, the two companies traded more independently, producing a noisier and less structured spread. Post-2020, Shell has structurally diverged from BP, pivoting more aggressively toward LNG and commanding a higher valuation multiple, causing the spread to trend persistently upward with no mean-reverting anchor.
<img width="1196" height="597" alt="image" src="https://github.com/user-attachments/assets/03f29f42-267b-4bc5-9361-a80bdf77c1b6" />

## The cointegration-profitability paradox

A striking finding is that the only sub-period with statistically significant cointegration (2010–2020) produces the worst trading performance: the lowest Sharpe ratio (0.164) and the largest maximum drawdown (-691.3). The non-cointegrated periods generate higher Sharpe ratios despite lacking a theoretical foundation.

This apparent paradox reflects an important limitation of the strategy. Cointegration guarantees that the spread will eventually revert, but says nothing about the speed of reversion. The Deepwater Horizon dislocation reverted over years, not days, meaning the strategy entered positions and held them through enormous intermediate losses before the spread closed. A z-score signal with fixed thresholds has no mechanism for managing slow-reverting dislocations.

The positive PnL in non-cointegrated periods is explained by a different mechanism: the rolling z-score captures short-term noise around a drifting mean, generating frequent small trades that are profitable on average even without a true mean-reverting anchor. This is a weaker and less reliable effect, as evidenced by the sharp deterioration in the 2020-present period when the drift becomes too strong for noise-trading to overcome.

---

# Limitations

This strategy makes several simplifying assumptions that limit its real-world applicability:

- **No transaction costs**: bid-ask spreads, borrow costs for short positions, and market impact are ignored. High-frequency signal generation would erode returns substantially in practice.
- **Reversion speed**: the strategy does not estimate the half-life of mean reversion, which is critical for position sizing and risk management.
- **Fixed parameters**: entry/exit thresholds and rolling window are fixed rather than optimised or adapted to changing regimes.
- **Single pair**: results are specific to BP and Shell and may not generalise.
- **No stop losses**: the strategy has no mechanism for exiting a losing position before the z-score reverts, leading to large drawdowns during slow-reverting dislocations.
- **Unnormalised PnL and max drawdown**: the cumulative PnL and max drawdown are denominated in GBP per share of Shell held, not on any notional capital amount. Returns are typically normalised by capital allocated.

---

# Lessons learnt

This project reinforced the importance of:

- testing statistical assumptions rigorously before constructing a trading signal, rather than assuming they hold,
- using correct critical values for hypothesis tests: standard ADF critical values are inappropriate for residuals estimated from a regression,
- distinguishing between statistical significance and economic significance: cointegration is a necessary but not sufficient condition for a profitable pairs trading strategy,
- understanding that model performance can be positive for the wrong reasons: the rolling z-score generates profits in non-cointegrated regimes through a noise-trading mechanism entirely distinct from mean reversion,
- interpreting negative or mixed results honestly: the finding that BP and Shell are not robustly cointegrated over a 20-year horizon is more informative than a strategy that works by construction.
