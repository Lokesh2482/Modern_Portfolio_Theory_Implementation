import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import minimize


plt.style.use('ggplot')

# -------------------- PARAMETERS --------------------
NUM_TRADING_DAYS = 252
NUM_PORTFOLIOS = 10000
STOCKS = ['AAPL', 'WMT', 'TSLA', 'GE', 'AMZN', 'DB']
START_DATE = '2010-01-01'
END_DATE = '2017-01-01'

# -------------------- DATA DOWNLOAD --------------------
def download_data(stocks):
    df = pd.DataFrame()
    for stock in stocks:
        ticker = yf.Ticker(stock)
        df[stock] = ticker.history(start=START_DATE, end=END_DATE)['Close']
    return df

# -------------------- DATA VISUALIZATION --------------------
def plot_price_history(data):
    plt.figure(figsize=(12, 6))
    for stock in data.columns:
        plt.plot(data.index, data[stock], label=stock)
    plt.title("Stock Price History")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.legend()
    plt.show()

# -------------------- RETURNS --------------------
def compute_log_returns(data):
    return np.log(data / data.shift(1)).dropna()

# -------------------- STATISTICS --------------------
def portfolio_performance(weights, returns):
    mean_return = np.sum(weights * returns.mean()) * NUM_TRADING_DAYS
    volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * NUM_TRADING_DAYS, weights)))
    sharpe_ratio = mean_return / volatility
    return mean_return, volatility, sharpe_ratio

# -------------------- PORTFOLIO SIMULATION --------------------
def simulate_portfolios(returns, num_portfolios=NUM_PORTFOLIOS):
    results = np.zeros((3, num_portfolios))
    weights_record = []

    for i in range(num_portfolios):
        weights = np.random.random(len(returns.columns))
        weights /= np.sum(weights)
        weights_record.append(weights)
        mean, vol, sharpe = portfolio_performance(weights, returns)
        results[0, i] = mean
        results[1, i] = vol
        results[2, i] = sharpe

    return np.array(weights_record), results

# -------------------- OPTIMIZATION --------------------
def neg_sharpe(weights, returns):
    return -portfolio_performance(weights, returns)[2]

def optimize_portfolio(returns):
    num_assets = len(returns.columns)
    args = (returns,)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0,1) for _ in range(num_assets))
    initial_guess = num_assets * [1./num_assets]
    opt = minimize(neg_sharpe, initial_guess, args=args, method='SLSQP', bounds=bounds, constraints=constraints)
    return opt

# -------------------- VISUALIZATIONS --------------------
def plot_efficient_frontier(results, weights_record, optimal):
    plt.figure(figsize=(12, 6))
    plt.scatter(results[1,:], results[0,:], c=results[2,:], cmap='viridis', marker='o', alpha=0.5)
    plt.colorbar(label='Sharpe Ratio')
    
    # Optimal point
    mean_opt, vol_opt, _ = portfolio_performance(optimal.x, log_returns)
    plt.scatter(vol_opt, mean_opt, color='r', marker='*', s=300, label='Max Sharpe Ratio')
    plt.title("Efficient Frontier & Optimal Portfolio")
    plt.xlabel("Volatility (Std Dev)")
    plt.ylabel("Expected Return")
    plt.legend()
    plt.show()

def plot_weights_pie(weights, labels):
    plt.figure(figsize=(8, 8))
    plt.pie(weights, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Optimal Portfolio Allocation")
    plt.show()

def plot_cumulative_returns(data, optimal_weights):
    cumulative_returns = (data.pct_change().dropna() + 1).cumprod()
    portfolio_cum_returns = (cumulative_returns @ optimal_weights)
    plt.figure(figsize=(12,6))
    plt.plot(cumulative_returns.index, portfolio_cum_returns, label='Optimal Portfolio', linewidth=2.5, color='black')
    for stock in cumulative_returns.columns:
        plt.plot(cumulative_returns.index, cumulative_returns[stock], alpha=0.5, label=stock)
    plt.title("Cumulative Returns Comparison")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.legend()
    plt.show()

def plot_correlation_heatmap(data):
    plt.figure(figsize=(8,6))
    sns.heatmap(data.corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Stock Correlation Matrix")
    plt.show()

# -------------------- MAIN EXECUTION --------------------
if __name__ == "__main__":
    # Download & visualize data
    data = download_data(STOCKS)
    plot_price_history(data)
    plot_correlation_heatmap(data)

    # Calculate returns
    log_returns = compute_log_returns(data)

    # Simulate portfolios
    weights_record, results = simulate_portfolios(log_returns)

    # Optimize portfolio
    optimal = optimize_portfolio(log_returns)
    optimal_mean, optimal_vol, optimal_sharpe = portfolio_performance(optimal.x, log_returns)
    
    print("Optimal Portfolio Weights:", np.round(optimal.x, 3))
    print("Expected Annual Return: {:.2f}%".format(optimal_mean*100))
    print("Expected Annual Volatility: {:.2f}%".format(optimal_vol*100))
    print("Sharpe Ratio: {:.2f}".format(optimal_sharpe))

    # Visualizations
    plot_efficient_frontier(results, weights_record, optimal)
    plot_weights_pie(optimal.x, STOCKS)
    plot_cumulative_returns(data, optimal.x)

