# portfolio_optimizer/reporting.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

class PortfolioReporter:
    """
    A reporting engine for formatting portfolio performance, 
    generating comparison tables, and plotting visual charts.
    """
    def __init__(self, asset_names, rf_rate):
        """
        Initialize the reporter with asset names and risk-free rate.
        """
        self.assets = list(asset_names)
        self.rf = rf_rate
        plt.style.use('seaborn-v0_8-darkgrid')

    def calc_performance(self, w, mu, cov):
        """
        Calculate Return, Volatility, and Sharpe Ratio for given weights.
        """
        r = float(w @ mu)
        v = float(np.sqrt(w @ cov @ w))
        s = (r - self.rf) / (v + 1e-12)
        return r, v, s

    def create_summary_table(self, portfolios_dict, mu, cov):
        """
        Generate a performance summary DataFrame.
        
        :param portfolios_dict: dict of {'Portfolio Name': weights_array}
        """
        data = []
        for name, w in portfolios_dict.items():
            r, v, s = self.calc_performance(w, mu, cov)
            data.append({'Portfolio': name, 'Return': r, 'Volatility': v, 'Sharpe': s})
            
        df = pd.DataFrame(data).set_index('Portfolio')
        return df

    def format_performance_table(self, df):
        """
        Format the performance DataFrame for clean display (percentages and decimals).
        """
        out = df.copy()
        out['Return'] = out['Return'].astype(float).map(lambda x: f'{x:.2%}')
        out['Volatility'] = out['Volatility'].astype(float).map(lambda x: f'{x:.2%}')
        out['Sharpe'] = out['Sharpe'].astype(float).map(lambda x: f'{x:.4f}')
        return out

    def plot_weights_grouped(self, weights_df, title="Portfolio Weights Comparison"):
        """
        Plot a grouped bar chart for portfolio weights.
        """
        cols = weights_df.columns.tolist()
        x = np.arange(len(self.assets))
        width = 0.85 / len(cols)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        for i, c in enumerate(cols):
            ax.bar(x + i * width, weights_df[c].values, width, label=c)
            
        ax.set_xticks(x + width * (len(cols) - 1) / 2)
        ax.set_xticklabels(self.assets, rotation=30, ha='right')
        ax.yaxis.set_major_formatter(PercentFormatter(1))
        ax.set_ylabel('Weight')
        ax.set_title(title, fontsize=14)
        ax.legend()
        plt.tight_layout()
        plt.show()

    def plot_allocation_pie(self, weights_series, title="Recommended Allocation", save_path=None):
        """
        Plot a highly customized pie chart for final asset allocation.
        Drops assets with weights < 0.01%.
        """
        weights = weights_series[weights_series > 0.0001].sort_values(ascending=False)
        colors = ['#FF8F00', '#4CAF50', '#D32F2F', '#7B1FA2', '#795548']
        
        # Make sure we have enough colors
        if len(weights) > len(colors):
            import matplotlib.cm as cm
            colors = cm.get_cmap('tab20').colors[:len(weights)]
            
        fig, ax = plt.subplots(figsize=(10, 8), facecolor='none')
        wedges, texts, autotexts = ax.pie(
            weights, 
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            pctdistance=0.8,
            textprops=dict(color="white", weight="bold", size=14),
            wedgeprops=dict(edgecolor='black')
        )

        legend = ax.legend(wedges, weights.index,
                           title="Asset Classes",
                           loc="center left",
                           bbox_to_anchor=(1, 0, 0.5, 1),
                           fontsize=12,
                           facecolor='black',    
                           edgecolor='white',    
                           labelcolor='white')
        plt.setp(legend.get_title(), color='white', weight='bold')

        ax.set_title(title, fontsize=16, pad=20, color="white" if save_path else "black")
        ax.axis('equal')  
        
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight', transparent=True)
            print(f"Pie chart saved to {save_path}")
            
        plt.show()
