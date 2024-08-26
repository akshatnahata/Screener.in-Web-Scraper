import yfinance as yf
import numpy as np
import pandas as pd
from scipy.stats import linregress

def calculate_alpha_beta(stock_data, market_data, risk_free_rate=0.0):
    # Calculate daily returns
    stock_returns = stock_data['Adj Close'].pct_change().dropna()
    market_returns = market_data['Adj Close'].pct_change().dropna()

    # Align the indices to make sure both series have the same number of data points
    aligned_data = pd.concat([stock_returns, market_returns], axis=1).dropna()
    stock_returns_aligned = aligned_data.iloc[:, 0]
    market_returns_aligned = aligned_data.iloc[:, 1]

    # Perform linear regression (slope=beta, intercept=alpha)
    slope, intercept, r_value, p_value, std_err = linregress(market_returns_aligned, stock_returns_aligned)
    
    # Beta from regression
    beta = slope

    # Expected return using CAPM
    # expected_return = risk_free_rate + beta * (market_returns_aligned.mean() - risk_free_rate)
    expected_return = risk_free_rate
    
    # Calculate alpha based on CAPM
    alpha = stock_returns_aligned.mean() - expected_return
    
    return alpha, beta

# Example usage
stock_symbol = 'TRENT.NS'
market_symbol = '^NSEI'  # S&P 500 index

# Download data
stock_data = yf.download(stock_symbol, start='2020-01-01', end='2024-08-01')
market_data = yf.download(market_symbol, start='2020-01-01', end='2024-08-01')

# Calculate alpha and beta
alpha, beta = calculate_alpha_beta(stock_data, market_data, risk_free_rate=0.02/252)  # Assuming 2% annual risk-free rate

print(f"Alpha: {alpha*100}")
print(f"Beta: {beta}")
