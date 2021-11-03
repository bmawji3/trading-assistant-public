import numpy as np  		   	 		  		  		    	 		 		   		 		  
import pandas as pd
from pandas import DataFrame, Series

def sma (
    ohlcv: DataFrame, 
    window: int = 20, 
    price_col: str = "close",
    ) -> Series:
    """
    Simple Moving Average. The most basic technical indicator.
    """

    return pd.Series(
        ohlcv[price_col].rolling(window).mean(),
        name="SMA{}".format(window),
    )


def ema (
    ohlcv: DataFrame, 
    window: int = 20, 
    price_col: str = "close",
    ) -> Series:
    """
    Exponential Weighted Moving Average.
    """

    return pd.Series(
        ohlcv[price_col].ewm(span=window).mean(),
        name="EMA{}".format(window),
    )

def vama (
    ohlcv: DataFrame, 
    window: int = 20, 
    price_col: str = "close",
    ) -> Series:
    """
    Volume Adjusted Moving Average.
    """
    vol_price = ohlcv["volume"] * ohlcv[price_col]
    vol_sum = ohlcv["volume"].rolling(window).mean()
    vol_ratio = pd.Series(vol_price/vol_sum, name="VAMA")
    cumSum = (vol_ratio * ohlcv[price_col]).rolling(window).sum()
    cumDiv = vol_ratio.rolling(window).sum()

    return pd.Series(cumSum / cumDiv,
        name="VAMA{}".format(window),
    )
