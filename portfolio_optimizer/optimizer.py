# portfolio_optimizer/optimizer.py
import numpy as np
from scipy.optimize import minimize
from .utils import nearest_psd, port_perf # import your own utilities

class StaticOptimizer:
    """
    A unified optimization engine for static portfolio allocation.
    """
    def __init__(self, mu, cov_matrix):
        self.mu = np.array(mu, dtype=float)
        # Repair the covariance matrix at initialization to ensure robustness
        self.cov = nearest_psd(cov_matrix)
        self.n_assets = len(self.mu)

    def maximize_sharpe(self, rf, bounds, constraints, w0=None):
        """Maximize Sharpe = (mu - rf) / sigma."""
        if w0 is None:
            w0 = np.full(self.n_assets, 1.0 / self.n_assets)
            
        def neg_sharpe(w):
            r, v = port_perf(w, self.mu, self.cov)
            return - (r - rf) / (v + 1e-12)
            
        result = minimize(neg_sharpe, w0, method='SLSQP',
                          bounds=bounds, constraints=constraints())
        return result

    def minimize_variance(self, bounds, constraints, w0=None):
        """Minimum variance portfolio under constraints."""
        if w0 is None:
            w0 = np.full(self.n_assets, 1.0 / self.n_assets)
            
        result = minimize(lambda w: port_perf(w, self.mu, self.cov)[1], w0, 
                          method='SLSQP', bounds=bounds, constraints=constraints())
        return result

    def target_return(self, target, bounds, constraints, w0=None):
        """Minimum variance subject to reaching at least target return."""
        if w0 is None:
            w0 = np.full(self.n_assets, 1.0 / self.n_assets)
            
        # Dynamically append the target return constraint
        cons = list(constraints()) + [{'type': 'ineq', 'fun': lambda w, t=target: w @ self.mu - t}]
        result = minimize(lambda w: port_perf(w, self.mu, self.cov)[1], w0, 
                          method='SLSQP', bounds=bounds, constraints=cons)
        return result
