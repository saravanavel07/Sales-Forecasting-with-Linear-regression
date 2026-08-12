# Sales Forecasting with Linear Regression

Predict future sales using a simple and interpretable Linear Regression pipeline built in Python.

Badges
- Build / CI: ![CI](https://img.shields.io/badge/ci-none-lightgrey)
- Python: ![Python](https://img.shields.io/badge/python-3.8%2B-blue)
- License: ![MIT](https://img.shields.io/badge/license-MIT-green)

Table of Contents
- [About](#about)
- [Features](#features)
- [Demo / Example Output](#demo--example-output)
- [Repository Structure](#repository-structure)
- [Requirements](#requirements)
- [Getting Started](#getting-started)
  - [Install](#install)
  - [Prepare Data](#prepare-data)
  - [Train Model](#train-model)
  - [Evaluate Model](#evaluate-model)
- [How it Works](#how-it-works)
- [Results & Metrics](#results--metrics)
- [Reproducibility](#reproducibility)
- [Notebooks](#notebooks)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

About
-----
This project demonstrates a complete, minimal pipeline for sales forecasting using Linear Regression (scikit-learn). It includes data loading, preprocessing, feature engineering, training, evaluation, and basic visualization to help you understand the end-to-end workflow.

Features
--------
- Clean, documented Python code for a reproducible forecasting pipeline.
- Data preprocessing (missing values, date-based features).
- Train/test splitting and cross-validation.
- Evaluation using MAE, MSE, RMSE, and R².
- Jupyter notebooks for exploration and visualization.
- Scripts to train and evaluate the model.

Demo / Example Output
---------------------
Example commands (assuming you place a CSV at `data/sales.csv`):
```bash
# train model
python src/train.py --data data/sales.csv --output models/linear_regression.joblib

# evaluate model
python src/eval.py --model models/linear_regression.joblib --data data/sales.csv
```

Typical evaluation metrics (example — replace with your run's numbers):
- MAE: 123.45
- RMSE: 234.56
- R²: 0.78

Repository Structure
--------------------
- data/                      # (gitignored) raw and processed datasets
- notebooks/                 # exploratory notebooks (EDA, feature engineering)
- src/
  - data_processing.py       # functions for cleaning and feature engineering
  - train.py                 # training script
  - eval.py                  # evaluation script
  - predict.py               # single-run inference / example usage
  - utils.py                 # helper functions
- models/                    # saved model artifacts
- requirements.txt
- README.md

Requirements
------------
- Python 3.8+
- See requirements.txt for the exact versions:
  - pandas
  - numpy
  - scikit-learn
  - matplotlib or seaborn (for visualizations)
  - joblib

Getting Started
---------------
1. Clone the repo:
```bash
git clone https://github.com/saravanavel07/Sales-Forecasting-with-Linear-regression.git
cd Sales-Forecasting-with-Linear-regression
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

3. Prepare your data:
- Place your sales CSV in `data/sales.csv` or pass a path to the script.
- CSV expectations (example columns):
  - date (YYYY-MM-DD)
  - store_id (optional)
  - item_id (optional)
  - sales (numeric) — target column
  - any other features (promotion, price, etc.)

Train Model
-----------
Train using the provided script:
```bash
python src/train.py --data data/sales.csv --target sales --date_col date --output models/linear_regression.joblib
```
Options:
- --data: path to CSV
- --target: name of target column (default: sales)
- --date_col: name of date column if present (optional)
- --output: path to save fitted model

Evaluate Model
--------------
Evaluate a saved model:
```bash
python src/eval.py --model models/linear_regression.joblib --data data/sales.csv --target sales
```
This prints MAE, MSE, RMSE, R² and saves a simple prediction vs actual plot to `reports/`.

How it Works
------------
1. Load CSV.
2. Parse dates and create date features (day, month, year, weekday).
3. Aggregate or filter by store/item if needed.
4. Fill missing values and scale features (if applicable).
5. Split to train/test (time-based split recommended for forecasting).
6. Train a scikit-learn LinearRegression model.
7. Evaluate with standard regression metrics.

Notes on Forecasting
--------------------
- Linear Regression is a baseline: it's fast and interpretable but may underperform complex time-series models.
- For time series forecasting, prefer time-based train/test split (no random shuffling).
- Consider lag features, rolling means, or using models like ARIMA, Prophet, or tree-based regressors for improved performance.

Results & Metrics
-----------------
- Use MAE (mean absolute error) and RMSE for interpretability in original units.
- R² gives a quick sense of variance explained.
- Cross-validate using time-series aware CV where appropriate (e.g., expanding window).

Reproducibility
---------------
- Seed random_state in train/test split and model training to make results reproducible.
- Save full preprocessing pipeline (e.g., with sklearn's Pipeline) alongside the model.
- Version datasets (store raw CSVs or use hashes) so experiments can be reproduced.

Notebooks
---------
See `notebooks/` for:
- EDA.ipynb — exploratory data analysis and visualization
- FeatureEngineering.ipynb — building lag/rolling features
- ModelComparison.ipynb — comparing Linear Regression vs alternatives

Contributing
------------
Contributions are welcome:
1. Fork the repo.
2. Create a feature branch (git checkout -b feature/your-feature).
3. Commit changes and open a pull request.
4. Ensure your code has clear documentation and, if applicable, tests.

Suggested improvements:
- Add unit tests for preprocessing.
- Add a CI workflow to run tests and style checks.
- Add hyperparameter tuning and better time-series CV.

License
-------
This project is provided under the MIT License. See LICENSE for details.

Contact
-------
Maintainer: saravanavel07
- GitHub: https://github.com/saravanavel07
- Email: (add your email here if you want to be contacted)

Acknowledgements
----------------
- Inspired by practical forecasting tutorials — adapt as needed for your dataset and business requirements.
