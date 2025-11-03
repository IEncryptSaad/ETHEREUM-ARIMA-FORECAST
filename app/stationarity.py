import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller, acf, pacf

# Perform ADF stationarity test
def adf_test(series: pd.Series):
    result = adfuller(series.dropna())
    labels = [
        "ADF Statistic", "p-value", "# Lags Used", "# Observations Used"
    ]
    output = pd.Series(result[0:4], index=labels)
    return output, result[1] <= 0.05  # stationary if p <= 0.05

# Plot ACF and PACF
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt

def plot_acf_pacf(series, lags=40):
    s = series.dropna()
    if len(s) > 800:  # keep plots light
        s = s.tail(800)
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    plot_acf(s, lags=lags, ax=ax[0])
    plot_pacf(s, lags=lags, ax=ax[1], method="ywm")
    plt.tight_layout()
    return fig
    
# Streamlit section
def run_stationarity_app(df: pd.DataFrame):
    st.header("📉 Stationarity Analysis (ADF + ACF/PACF)")
    target = "close"
    st.write("Using column:", target)

    series = df[target]

    # Run ADF test
    output, stationary = adf_test(series)
    st.subheader("ADF Test Results")
    st.dataframe(output)
    if stationary:
        st.success("✅ Series appears stationary (p ≤ 0.05).")
    else:
        st.warning("⚠️ Series is likely non-stationary (p > 0.05). Differencing may be required.")

    # Plot ACF/PACF
    st.subheader("ACF and PACF Plots")
    st.pyplot(plot_acf_pacf(series))
