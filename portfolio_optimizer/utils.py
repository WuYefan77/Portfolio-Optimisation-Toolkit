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
