# portfolio_optimizer/constraints.py
import numpy as np

def create_style_constraints(asset_names, style_assets, w_low, w_high):
    """
    Build style constraints for a given asset ordering.
    Keeps a specific bucket of assets between [w_low, w_high].
    """
    aset = list(asset_names)
    # Only include assets that are actually in the provided asset_names list
    g_idx = [aset.index(a) for a in style_assets if a in aset]  

    def _constraints():
        return (
            {'type': 'eq',   'fun': lambda w: np.sum(w) - 1.0}, # Sum of weights = 1
            {'type': 'ineq', 'fun': lambda w: np.sum(w[g_idx]) - w_low}, # Min style weight
            {'type': 'ineq', 'fun': lambda w: w_high - np.sum(w[g_idx])}, # Max style weight
        )
    return _constraints
