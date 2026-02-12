from pypfopt import HRPOpt, CLA, risk_models, expected_returns, objective_functions
from pypfopt.efficient_frontier import EfficientFrontier
import numpy as np
import pandas as pd

# Configuration
METHOD = 'ledoit_wolf'
GAMMA = 0

# Helper Functions
def get_risk_parameters(df):
    mu = expected_returns.mean_historical_return(df)
    sigma = risk_models.risk_matrix(df, method=METHOD)
    mu_ema = expected_returns.ema_historical_return(df, span=252, frequency=252)
    sigma_ew = risk_models.exp_cov(df, span=180, frequency=252)
    return mu, sigma, mu_ema, sigma_ew

def clean_weights(ef, label):
    clean = ef.clean_weights()
    return pd.DataFrame.from_dict(clean, columns=[label], orient='index')

# Portfolio Optimization Models
def minvol(df_stocks):
    mu, sigma, _, _ = get_risk_parameters(df_stocks)
    ef = EfficientFrontier(mu, sigma)
    ef.min_volatility()
    return clean_weights(ef, 'Min Volatility')

def ew_minvol(df_stocks):
    _, _, mu_ema, sigma_ew = get_risk_parameters(df_stocks)
    ef_ew = EfficientFrontier(mu_ema, sigma_ew)
    ef_ew.min_volatility()
    return clean_weights(ef_ew, 'EW Min Vol')

def maxsharpe(df_stocks):
    mu, sigma, _, _ = get_risk_parameters(df_stocks)
    ef = EfficientFrontier(mu, sigma)
    ef.max_sharpe()
    return clean_weights(ef, 'Max Sharpe')

def ew_maxsharpe(df_stocks):
    _, _, mu_ema, sigma_ew = get_risk_parameters(df_stocks)
    ef_ew = EfficientFrontier(mu_ema, sigma_ew)
    ef_ew.max_sharpe()
    return clean_weights(ef_ew, 'EW Max Sharpe')

def non_convex(df_stocks):
    mu, sigma, _, _ = get_risk_parameters(df_stocks)
    ef = EfficientFrontier(mu, sigma)
    ef.nonconvex_objective(deviation_risk_parity, ef.cov_matrix)
    return clean_weights(ef, 'Non Convex')

def cla_max(df_stocks):
    mu, sigma, _, _ = get_risk_parameters(df_stocks)
    ef_cla = CLA(mu, sigma)
    ef_cla.max_sharpe()
    return clean_weights(ef_cla, 'CLA Max Sharpe')

def HRP(df_stocks):
    df_returns = df_stocks.pct_change().dropna()
    hrp = HRPOpt(df_returns, risk_models.risk_matrix(df_stocks, method=METHOD))
    hrp.optimize()
    clean = hrp.clean_weights()
    return pd.DataFrame.from_dict(clean, columns=['HRP'], orient='index')

def df_equal(df_stocks):
    clean = np.full(df_stocks.shape[1], 1/df_stocks.shape[1])
    return pd.DataFrame(clean, columns=['Equal'], index=df_stocks.columns)

# Objective Functions
def objective_sharpe_gamma(w, mu, s):
    return objective_functions.sharpe_ratio(w, mu, s) + objective_functions.L2_reg(w, gamma=GAMMA)

def deviation_risk_parity(w, cov_matrix):
    diff = w * np.dot(cov_matrix, w) - (w * np.dot(cov_matrix, w)).reshape(-1, 1)
    return np.sum(diff ** 2)

# Main Optimization Function
def optimize(df_stocks):
    models = [
        minvol(df_stocks), ew_minvol(df_stocks), maxsharpe(df_stocks), ew_maxsharpe(df_stocks),
        non_convex(df_stocks), cla_max(df_stocks), HRP(df_stocks), df_equal(df_stocks)
    ]
    return pd.concat(models, axis=1)
