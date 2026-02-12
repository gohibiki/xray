import numpy as np
import pandas as pd
from datetime import datetime

def calculate_cagr(start, end, periods):
    return (end / start) ** (1 / periods) - 1

def calculate_std_dev(returns):
    return returns.std() * np.sqrt(252)

def calculate_best_year(returns):
    yearly_returns = returns.resample('Y').apply(lambda x: (1 + x).prod() - 1)
    return yearly_returns.max()

def calculate_worst_year(returns):
    yearly_returns = returns.resample('Y').apply(lambda x: (1 + x).prod() - 1)
    return yearly_returns.min()

def calculate_ytd_return(prices):
    """Calculate year-to-date return"""
    current_year = prices.index[-1].year
    year_start_price = prices[prices.index.year == current_year].iloc[0]
    latest_price = prices.iloc[-1]
    return (latest_price / year_start_price - 1) * 100

def calculate_period_return(prices, years):
    """Calculate return for a specific period in years"""
    if len(prices) < years * 252:  # Approximate trading days in a year
        return np.nan
    
    end_date = prices.index[-1]
    if years == 1:
        start_date = end_date - pd.DateOffset(years=1)
    else:
        start_date = end_date - pd.DateOffset(years=years)
    
    # Find the closest dates
    start_price = prices.loc[prices.index >= start_date].iloc[0]
    end_price = prices.iloc[-1]
    
    total_return = (end_price / start_price - 1) * 100
    
    # Only annualize if period is greater than 1 year
    if years > 1:
        return ((1 + total_return/100) ** (1/years) - 1) * 100
    return total_return

def calculate_metrics(prices_df, returns_df=None, weights_df=None):
    metrics = {}
    
    if weights_df is not None and returns_df is not None:
        for col in weights_df.columns:
            portfolio_returns = returns_df.dot(weights_df[col])
            prices = (1 + portfolio_returns).cumprod()
            start_value = prices.iloc[0]
            end_value = prices.iloc[-1]
            periods = (prices.index[-1] - prices.index[0]).days / 365.25
            
            metrics[col] = calculate_individual_metrics(
                start_value, end_value, periods, portfolio_returns, prices
            )
    else:
        for column in prices_df.columns:
            prices = prices_df[column].interpolate(method='linear')
            returns = prices.pct_change().dropna()
            start_value = prices.iloc[0]
            end_value = prices.iloc[-1]
            periods = (prices.index[-1] - prices.index[0]).days / 365.25
            
            metrics[column] = calculate_individual_metrics(
                start_value, end_value, periods, returns, prices
            )
            
    metrics_df = pd.DataFrame(metrics).T
    return metrics_df.round(2).map(lambda x: f"{x:.2f}" if pd.notnull(x) else x)

def calculate_individual_metrics(start_value, end_value, periods, returns, prices):
    return {
        'Vol.': calculate_std_dev(returns) * 100,
        '1m': calculate_period_return(prices, 1),
        '3m': calculate_period_return(prices, 3),
        'YTD': calculate_ytd_return(prices),
        '1yr': calculate_period_return(prices, 1),
        '3yr': calculate_period_return(prices, 3),
        '5yr': calculate_cagr(start_value, end_value, periods) * 100
    }