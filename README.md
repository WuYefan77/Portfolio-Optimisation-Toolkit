# Static Portfolio Optimization Toolkit

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An institutional-grade, object-oriented Python toolkit for **Mean-Variance Portfolio Optimization**. This library is designed for constructing and stress-testing Strategic Asset Allocations (SAA) under complex, real-world constraints.

---

## Core Features
* **Advanced Optimization Engine**: Core solvers for Maximum Sharpe Ratio (MSR), Global Minimum Variance (GMVP), and Target Return portfolios using `scipy.optimize.minimize` (SLSQP).
* **Robust Risk Modeling**: Built-in utility using **Eigenvalue Clipping** to mathematically repair non-Positive Semi-Definite (non-PSD) covariance matrices, essential for stress-testing and handling flawed market data.
* **Dynamic Constraint Factory**: A functional approach to easily generate complex business rules, such as long-only, position caps, and style-band constraints (e.g., Growth vs. Defensive).
* **Automated Reporting Module**: A dedicated `PortfolioReporter` class to instantly generate publication-ready performance tables and stylized allocation charts.

---

## Project Architecture

This project follows a decoupled, professional software engineering design pattern, separating quantitative logic from presentation:

```text
Portfolio-Optimization-Toolkit/
├── portfolio_optimizer/       # Core Python Package (Optimization Engine)
│   ├── __init__.py
│   ├── utils.py               # Low-level math (PSD fix, portfolio moments)
│   ├── constraints.py         # Business logic & constraint factories
│   ├── optimizer.py           # OOP-based optimization engine
│   └── reporting.py           # Presentation layer
├── 01_Static_Optimization_Showcase.ipynb  # Core usage demonstration
├── 02_Risk_Profile_Analysis.ipynb         # Utility & Risk profile comparison
├── 03_Model_Fragility_Test.ipynb          # Covariance breakdown & repair test
├── requirements.txt
└── README.md

---

## Installation

Clone the repository and install the required dependencies:

```bash
git clone [https://github.com/WuYefan77/Portfolio-Optimization-Toolkit.git](https://github.com/WuYefan77/Portfolio-Optimization-Toolkit.git)
cd Portfolio-Optimization-Toolkit
pip install -r requirements.txt
```

---

## Quick Start Example

The toolkit is designed for intuitive, OOP-based portfolio construction. Here is a minimal example:

```python
import numpy as np
from portfolio_optimizer.optimizer import StaticOptimizer

# 1. Define your market data
mu = np.array([0.10, 0.08, 0.04])
cov = np.array([
    [0.0225, 0.0135, 0.0015],
    [0.0135, 0.0144, 0.0024],
    [0.0015, 0.0024, 0.0025]
])

# 2. Initialize the engine (automatically validates/repairs covariance)
opt = StaticOptimizer(mu, cov)

# 3. Define basic constraints (e.g., long-only, 50% max position)
bounds = tuple((0.0, 0.50) for _ in range(3))
constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0})

# 4. Solve for Maximum Sharpe Ratio
result = opt.maximize_sharpe(rf=0.02, bounds=bounds, constraints=constraints)
print(f"Optimal Weights: {np.round(result.x, 4)}")
```

For more advanced use cases, including dynamic style-band constraints and Model Fragility (Non-PSD) stress testing, please refer to the Jupyter Notebooks in this repository.
