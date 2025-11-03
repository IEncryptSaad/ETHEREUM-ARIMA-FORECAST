# ETHEREUM ARIMA FORECAST

Cloud-based Ethereum (ETH/USDT) price forecasting app using ARIMA time series modeling.
Built with Streamlit, Python, and Binance public API for historical data.
Fully deployed on Streamlit Community Cloud — zero local storage.

## Features
- Fetch ETH/USDT OHLCV from Binance (public, no key)
- EDA: trends, volatility, rolling stats
- Stationarity testing (ADF) + ACF/PACF
- ARIMA modeling (manual grid + optional auto-ARIMA)
- Residual diagnostics and backtest metrics (RMSE, MAPE)
- 30-day forecast with confidence intervals

## Run (Streamlit Cloud)
Deploy this repo directly on Streamlit Community Cloud.

## Project layout (planned)
- app/
  - Home.py
  - data_fetch.py
  - eda.py
  - stationarity.py
  - modeling.py
  - evaluate.py
- requirements.txt
- .gitignore
- .streamlit/
  - config.toml

## IMPLEMENTATION DETAILS
This project demonstrates an end-to-end approach to cryptocurrency time series forecasting using ARIMA. It integrates live market data retrieval, exploratory data analysis, stationarity testing, model training, and future price forecasting within an interactive cloud-based application.

### 1. DATA PIPELINE
- Historical OHLCV data is retrieved using the Binance public API.
- If Binance is restricted, the application automatically falls back to CoinGecko’s OHLC endpoint.
- Data is preprocessed into a time-indexed pandas DataFrame for further analysis.

### 2. EXPLORATORY ANALYSIS
- Line charts visualize Ethereum’s closing prices over time.
- Summary statistics highlight trends, volatility, and data completeness.
- Recent historical data is displayed in a scrollable DataFrame within Streamlit.

### 3. STATIONARITY TESTING
- The Augmented Dickey-Fuller (ADF) test is applied to determine if differencing is required.
- The Autocorrelation Function (ACF) and Partial Autocorrelation Function (PACF) plots assist in identifying AR and MA terms.
- Non-stationary results (p > 0.05) indicate the need for differencing before ARIMA modeling.

### 4. ARIMA MODELING
- Users can interactively select ARIMA parameters (p, d, q) through the interface.
- The model is trained on the historical close price data.
- Key metrics (RMSE and MAPE) are calculated using a hold-out validation set.
- The trained model generates forward forecasts for a user-defined horizon.

### 5. FORECAST VISUALIZATION
- Forecasted prices are plotted against historical data to highlight short-term and long-term trends.
- Users can adjust forecast horizons dynamically (default: 30 days).
- Forecast results are displayed in tabular form for clarity.

### 6. DATA EXPORT
- The forecasted values, along with corresponding timestamps, can be downloaded as a CSV file for offline analysis or reporting.
- This feature ensures compatibility with external analytics workflows such as Excel, Power BI, or Jupyter.

### 7. CLOUD DEPLOYMENT
- The app is deployed on Streamlit Community Cloud for free and requires no local setup.
- Dependencies are managed automatically from the `requirements.txt` file.
- The `.streamlit/config.toml` file defines the project’s dark theme and typography.

### 8. TECHNOLOGIES USED
- Python 3.10+
- Streamlit
- pandas, numpy, matplotlib
- statsmodels (ARIMA)
- scikit-learn (evaluation metrics)
- requests (API handling)

### 9. FUTURE ENHANCEMENTS
- Extend support for additional cryptocurrencies (BTC, SOL, ADA, etc.)
- Integrate SARIMA or Prophet for seasonal forecasting.
- Include volatility and correlation analysis for multi-asset insights.
- Implement automated model selection and parameter optimization.

### 10. AUTHOR AND ACKNOWLEDGMENT
Developed by **Saad Bin Masud**  
Machine Learning Internship Project – **Arch Technologies**

