import pandas as pd
import requests
from datetime import datetime

# Fetch ETH/USDT historical price data from Binance public API
def get_binance_data(symbol="ETHUSDT", interval="1h", limit=500):
    """
    Fetch OHLCV (Open, High, Low, Close, Volume) data for the given symbol.
    interval: '1h', '4h', '1d', etc.
    limit: number of candles (max 1000 per request)
    """
    url = f"https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    df = pd.DataFrame(
        data,
        columns=[
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "num_trades",
            "taker_buy_base", "taker_buy_quote", "ignore"
        ],
    )

    # Convert to proper datatypes
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")
    numeric_cols = ["open", "high", "low", "close", "volume"]
    df[numeric_cols] = df[numeric_cols].astype(float)

    return df[["open_time", "open", "high", "low", "close", "volume"]]
