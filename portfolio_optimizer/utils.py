# portfolio_optimizer/utils.py
import numpy as np

def nearest_psd(A, tol=1e-12):
    """
    Make a symmetric matrix positive semi-definite by clipping tiny negative eigenvalues.
    Essential for robust optimization with noisy financial data.
    """
    A = np.asarray(A)
    B = (A + A.T) / 2
    w, V = np.linalg.eigh(B)
    w[w < tol] = tol
    return V @ np.diag(w) @ V.T

def port_perf(w, mu, S):
    """
    Return (expected return, volatility) for given weights w.
    """
    r = float(w @ mu)
    v = float(np.sqrt(w @ S @ w))
    return r, v

def exp_utility(mu, sigma, gamma=1.0):
    """
    Calculate the Exponential (CARA) utility: E[U] = -exp(-γ(μ - 0.5 γ σ^2)).
    Used for assessing investor satisfaction under different risk profiles.
    """
    return -np.exp(-gamma * (mu - 0.5 * gamma * sigma**2))
