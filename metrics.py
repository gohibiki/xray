import numpy as np
import pandas as pd
from datetime import datetime

def calculate_cagr(start, end, periods):
    """Calculate Compound Annual Growth Rate"""
    try:
        if start <= 0 or end <= 0 or periods <= 0:
            return np.nan
        return (end / start) ** (1 / periods) - 1
    except (ZeroDivisionError, ValueError, OverflowError):
        return np.nan

def calculate_std_dev(returns):
    return returns.std() * np.sqrt(252)

def calculate_sharpe_ratio(returns, risk_free_rate=0):
    """Calculate annualized Sharpe Ratio"""
    excess_returns = returns - risk_free_rate
    return (excess_returns.mean() / returns.std()) * np.sqrt(252) if returns.std() != 0 else 0

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

def calculate_period_return(prices, months):
    """Calculate return for a specific period in months"""
    if len(prices) < 2:
        return np.nan

    end_date = prices.index[-1]
    start_date = end_date - pd.DateOffset(months=months)

    # Find the closest date on or after start_date
    valid_dates = prices.loc[prices.index >= start_date]
    if len(valid_dates) == 0:
        return np.nan

    start_price = valid_dates.iloc[0]
    end_price = prices.iloc[-1]

    total_return = (end_price / start_price - 1) * 100

    # Annualize if period is 12 months or more
    if months >= 12:
        years = months / 12
        return ((1 + total_return/100) ** (1/years) - 1) * 100
    return total_return

def calculate_metrics(prices_df, returns_df=None, weights_df=None):
    metrics = {}
    
    if weights_df is not None and returns_df is not None:
        for col in weights_df.columns:
            portfolio_returns = returns_df.dot(weights_df[col])
            # Remove NaN values before cumulative product
            portfolio_returns_clean = portfolio_returns.dropna()
            prices = (1 + portfolio_returns_clean).cumprod()
            start_value = prices.iloc[0]
            end_value = prices.iloc[-1]
            periods = (prices.index[-1] - prices.index[0]).days / 365.25

            metrics[col] = calculate_individual_metrics(
                start_value, end_value, periods, portfolio_returns_clean, prices
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
    # Format numbers with 2 decimal places, show "N/A" for missing values
    return metrics_df.map(lambda x: f"{x:.2f}" if pd.notnull(x) and isinstance(x, (int, float)) else "N/A" if pd.isnull(x) else x)

def calculate_individual_metrics(start_value, end_value, periods, returns, prices):
    # Calculate annualized return (CAGR) for whatever period is available
    # Handle edge cases: check if we have valid start/end values and sufficient period
    if periods > 0 and start_value > 0 and end_value > 0 and not np.isnan(start_value) and not np.isnan(end_value):
        cagr = calculate_cagr(start_value, end_value, periods) * 100
    else:
        cagr = np.nan

    return {
        'Sharpe': calculate_sharpe_ratio(returns),
        'Vol.': calculate_std_dev(returns) * 100,
        '1m': calculate_period_return(prices, 1),
        '3m': calculate_period_return(prices, 3),
        'YTD': calculate_ytd_return(prices),
        '1yr': calculate_period_return(prices, 12),
        '3yr': calculate_period_return(prices, 36),
        '5yr': cagr
    }