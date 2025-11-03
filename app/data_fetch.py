import math
import time
import pandas as pd
import requests

BINANCE_URL = "https://api.binance.com/api/v3/klines"
COINGECKO_OHLC_URL = "https://api.coingecko.com/api/v3/coins/ethereum/ohlc"

class DataFetchError(Exception):
    pass

# ---------- helpers

def _http_get(url, params, max_retries=4, base_sleep=1.5):
    """GET with basic backoff. Retries 429/5xx, sets a UA header."""
    headers = {
        "User-Agent": "ETH-ARIMA-Cloud/1.0 (+https://streamlit.app)"
    }
    last_exc = None
    for attempt in range(max_retries):
        try:
            r = requests.get(url, params=params, headers=headers, timeout=12)
            # If 429 or 5xx, backoff and retry
            if r.status_code in (429, 500, 502, 503, 504):
                sleep = base_sleep * (2 ** attempt)
                time.sleep(sleep)
                continue
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            last_exc = e
            # brief backoff then retry
            time.sleep(base_sleep * (2 ** attempt))
    if last_exc:
        raise last_exc
    raise DataFetchError("HTTP GET failed with no response")

# ---------- main sources

def _binance_ohlcv(symbol="ETHUSDT", interval="1h", limit=500) -> pd.DataFrame:
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    r = _http_get(BINANCE_URL, params)
    data = r.json()
    df = pd.DataFrame(
        data,
        columns=[
            "open_time","open","high","low","close","volume",
            "close_time","quote_asset_volume","num_trades",
            "taker_buy_base","taker_buy_quote","ignore",
        ],
    )
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    for c in ["open","high","low","close","volume"]:
        df[c] = df[c].astype(float)
    return df[["open_time","open","high","low","close","volume"]]

def _round_days_allowed(days_required: int) -> int:
    # CoinGecko only accepts: 1, 7, 14, 30, 90, 180, 365, "max"
    allowed = [1, 7, 14, 30, 90, 180, 365]
    for d in allowed:
        if days_required <= d:
            return d
    return 365

def _coingecko_ohlc(interval: str, candles: int) -> pd.DataFrame:
    # Translate candles->days for CoinGecko
    if interval == "1h":
        days_needed = math.ceil(candles / 24)
    elif interval == "4h":
        days_needed = math.ceil(candles / 6)
    else:  # "1d"
        days_needed = max(1, candles)

    # Try a descending list of acceptable day buckets to dodge 429
    first = _round_days_allowed(days_needed)
    try_list = sorted({first, 30, 14, 7, 1}, reverse=True)  # e.g., 30,14,7,1

    last_exc = None
    for days in try_list:
        try:
            r = _http_get(COINGECKO_OHLC_URL, {"vs_currency": "usd", "days": days})
            rows = r.json()
            if not rows:
                continue
            df = pd.DataFrame(rows, columns=["ts","open","high","low","close"])
            df["open_time"] = pd.to_datetime(df["ts"], unit="ms")
            for c in ["open","high","low","close"]:
                df[c] = df[c].astype(float)
            df["volume"] = pd.NA  # endpoint has no volume
            # Keep only the most recent `candles` rows
            df = df[["open_time","open","high","low","close","volume"]].tail(candles)
            return df
        except Exception as e:
            last_exc = e
            continue
    raise DataFetchError(f"CoinGecko failed after retries: {last_exc}")

def get_eth_ohlcv(interval="1h", limit=500) -> pd.DataFrame:
    """
    Try Binance first. If legal block (451/403) or error, fall back to CoinGecko
    with retry/backoff and dynamic day buckets.
    """
    try:
        return _binance_ohlcv(symbol="ETHUSDT", interval=interval, limit=limit)
    except requests.HTTPError as e:
        status = getattr(e.response, "status_code", None)
        if status in (451, 403):
            return _coingecko_ohlc(interval, limit)
        # other HTTP errors: still try fallback
        return _coingecko_ohlc(interval, limit)
    except Exception:
        return _coingecko_ohlc(interval, limit)
