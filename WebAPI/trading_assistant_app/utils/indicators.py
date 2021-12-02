import numpy as np
import pandas as pd
from pandas import DataFrame, Series


def get_sma(
        ohlcv: DataFrame,
        window: int = 50,
        price_col: str = "close",
) -> Series:
    """
    Simple Moving Average. The most basic technical indicator.
    """

    return pd.Series(
        ohlcv[price_col].rolling(window=window, min_periods=window).mean(),
        name="SMA{}".format(window),
    )


def get_price_sma(
        ohlcv: DataFrame,
        window: int = 50,
        price_col: str = "close",
) -> Series:
    """
    Price to SMA.
    """

    return pd.Series(
        ohlcv[price_col] / get_sma(ohlcv, window),
        name="Price/SMA{}".format(window),
    )


def get_ema(
        ohlcv: DataFrame,
        window: int = 20,
        price_col: str = "close",
) -> Series:
    """
    Exponential Weighted Moving Average.
    """

    return pd.Series(
        ohlcv[price_col].ewm(span=window, adjust=False, min_periods=window).mean(),
        name="EMA{}".format(window),
    )


def get_vama(
        ohlcv: DataFrame,
        window: int = 20,
        price_col: str = "close",
) -> Series:
    """
    Volume Adjusted Moving Average.
    """
    vol_price = ohlcv["volume"] * ohlcv[price_col]
    vol_sum = ohlcv["volume"].rolling(window=window, min_periods=window).mean()
    vol_ratio = pd.Series(vol_price / vol_sum, name="VAMA")
    cum_sum = (vol_ratio * ohlcv[price_col]).rolling(window=window, min_periods=window).sum()
    cum_div = vol_ratio.rolling(window=window, min_periods=window).sum()

    return pd.Series(cum_sum / cum_div,
                     name="VAMA{}".format(window),
                     )


def get_bb_pct(
        ohlcv: DataFrame,
        window: int = 10,
        price_col: str = "close",
) -> Series:
    sma = get_sma(ohlcv, window)
    sma_std = ohlcv[price_col].rolling(window=window, min_periods=window).std()
    bb_low = sma - 2 * sma_std
    bb_up = sma + 2 * sma_std

    bb_pct = (ohlcv[price_col] - bb_low) / (bb_up - bb_low)

    return pd.Series(bb_pct,
                     name="BB%{}".format(window),
                     )


def get_rsi(
        ohlcv: DataFrame,
        window: int = 5,
        price_col: str = "close",
) -> Series:
    df = ohlcv[price_col]
    diff = df.diff()
    gain = diff.where(diff > 0, 0)
    loss = diff.where(diff < 0, 0)

    avg_gain = gain.rolling(window=window, min_periods=window).sum()
    avg_loss = 0 - loss.rolling(window=window, min_periods=window).sum()

    rs = avg_gain / avg_loss

    rsi = 100 - 100 / (1 + rs)

    return pd.Series(rsi,
                     name="RSI{}".format(window),
                     )


def get_momentum(
        ohlcv: DataFrame,
        window: int = 5,
        price_col: str = "close",
) -> Series:
    momentum = (ohlcv[price_col] / ohlcv[price_col].shift(window)) - 1

    return pd.Series(momentum,
                     name="MOM{}".format(window),
                     )


def get_macd_signal(
        ohlcv: DataFrame,
        signal_days: int = 9,
        price_col: str = "close",
) -> Series:
    ema_12 = get_ema(ohlcv, window=12)
    ema_26 = get_ema(ohlcv, window=26)
    macd = ema_12 - ema_26

    return pd.Series(macd.ewm(span=signal_days, adjust=False, min_periods=signal_days).mean(),
                     name="MACD{}".format(signal_days),
                     )
