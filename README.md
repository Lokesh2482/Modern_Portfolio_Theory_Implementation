# Portfolio Optimization & Efficient Frontier Analysis

This project demonstrates portfolio optimization using historical stock data. It simulates thousands of random portfolios, calculates performance metrics (expected return, volatility, Sharpe ratio), and finds the optimal portfolio with the maximum Sharpe ratio. Visualizations include stock price history, cumulative returns, correlation heatmaps, and the efficient frontier.

## Features

* Download historical stock price data using `yfinance`.
* Compute **log returns** for accurate portfolio performance metrics.
* Simulate **10,000 random portfolios** and calculate:

  * Expected annual return
  * Annual volatility
  * Sharpe ratio
* Optimize the portfolio to **maximize Sharpe ratio** using `scipy.optimize.minimize`.
* Visualizations:

  * Stock price history
  * Correlation heatmap
  * Efficient frontier with maximum Sharpe ratio highlighted
  * Optimal portfolio allocation (pie chart)
  * Cumulative returns comparison

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/portfolio-optimization.git
cd portfolio-optimization
```

2. Install required packages:

```bash
pip install numpy pandas matplotlib seaborn yfinance scipy
```

## Usage

1. Open `portfolio_optimization.py` in your favorite IDE.
2. Update stock symbols, start date, or end date if needed:

```python
STOCKS = ['AAPL', 'WMT', 'TSLA', 'GE', 'AMZN', 'DB']
START_DATE = '2010-01-01'
END_DATE = '2017-01-01'
```

3. Run the script:

```bash
python portfolio_optimization.py
```

4. Outputs:

* Console: Optimal portfolio weights, expected annual return, volatility, and Sharpe ratio.
* Visualizations: Efficient frontier, allocation pie chart, cumulative returns, and correlation heatmap.

## How It Works

1. **Data Download:** Fetches historical closing prices for the selected stocks.
2. **Return Calculation:** Computes log returns for more accurate financial modeling.
3. **Portfolio Simulation:** Generates random weights, calculates portfolio performance metrics for each simulation.
4. **Portfolio Optimization:** Uses the **Sharpe ratio** to identify the optimal asset allocation.
5. **Visualization:** Provides intuitive plots to understand risk-return trade-offs and diversification benefits.

## Example Output

```
Optimal Portfolio Weights: [0.25, 0.10, 0.30, 0.05, 0.20, 0.10]
Expected Annual Return: 15.23%
Expected Annual Volatility: 18.45%
Sharpe Ratio: 0.83
```

## Libraries Used

* [NumPy](https://numpy.org/) – Numerical computations
* [Pandas](https://pandas.pydata.org/) – Data manipulation
* [Matplotlib](https://matplotlib.org/) – Plotting
* [Seaborn](https://seaborn.pydata.org/) – Statistical visualization
* [yfinance](https://pypi.org/project/yfinance/) – Stock data download
* [SciPy](https://scipy.org/) – Optimization
