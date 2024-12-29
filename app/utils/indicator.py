import pandas as pd
import talib as ta


def calculate_ma(data: pd.Series, n: int) -> pd.Series:
    """计算移动平均线"""
    result = ta.MA(data, timeperiod=n)
    return pd.Series(result, index=data.index)


def calculate_macd(
    close: pd.Series,
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9,
) -> tuple[pd.Series, pd.Series, pd.Series]:
    """计算MACD指标"""
    diff, dea, macd = ta.MACD(
        close,
        fastperiod=fast_period,
        slowperiod=slow_period,
        signalperiod=signal_period,
    )
    return (
        pd.Series(diff, index=close.index),
        pd.Series(dea, index=close.index),
        pd.Series(macd * 2, index=close.index),
    )


def calculate_kdj(
    high: pd.Series, low: pd.Series, close: pd.Series, n: int = 9
) -> tuple[pd.Series, pd.Series, pd.Series]:
    """计算KDJ指标"""
    k, d = ta.STOCH(
        high,
        low,
        close,
        fastk_period=n,
        slowk_period=5,
        slowk_matype=1,
        slowd_period=5,
        slowd_matype=1,
    )
    k = pd.Series(k, index=close.index)
    d = pd.Series(d, index=close.index)
    j = 3 * k - 2 * d
    return k, d, j


def calculate_rsi(close: pd.Series, n: int = 14) -> pd.Series:
    """计算RSI指标"""
    result = ta.RSI(close, timeperiod=n)
    return pd.Series(result, index=close.index)


def calculate_boll(
    close: pd.Series, n: int = 20, k: float = 2
) -> tuple[pd.Series, pd.Series, pd.Series]:
    """计算布林带"""
    upper, middle, lower = ta.BBANDS(
        close, timeperiod=n, nbdevup=k, nbdevdn=k, matype=0
    )
    return (
        pd.Series(upper, index=close.index),
        pd.Series(middle, index=close.index),
        pd.Series(lower, index=close.index),
    )


def calculate_dmi(
    high: pd.Series, low: pd.Series, close: pd.Series, n: int = 14
) -> tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
    """计算DMI指标"""
    # 直接使用 talib 的 DMI 相关函数
    pdi = pd.Series(ta.PLUS_DI(high, low, close, timeperiod=n), index=close.index)
    mdi = pd.Series(ta.MINUS_DI(high, low, close, timeperiod=n), index=close.index)
    adx = pd.Series(ta.ADX(high, low, close, timeperiod=n), index=close.index)
    adxr = pd.Series(ta.ADXR(high, low, close, timeperiod=n), index=close.index)

    return pdi, mdi, adx, adxr


def calculate_trix(
    close: pd.Series, n: int = 12, m: int = 9
) -> tuple[pd.Series, pd.Series]:
    """计算TRIX指标"""
    trix = pd.Series(ta.TRIX(close, timeperiod=n), index=close.index)
    matrix = pd.Series(ta.MA(trix, timeperiod=m), index=close.index)
    return trix, matrix


def calculate_cci(
    high: pd.Series, low: pd.Series, close: pd.Series, n: int = 14
) -> pd.Series:
    """计算CCI指标"""
    result = ta.CCI(high, low, close, timeperiod=n)
    return pd.Series(result, index=close.index)

def calculate_dma(
    close: pd.Series, short: int = 10, long: int = 50, m: int = 10
) -> tuple[pd.Series, pd.Series]:
    """计算DMA指标"""
    ma_short = pd.Series(ta.MA(close, timeperiod=short), index=close.index)
    ma_long = pd.Series(ta.MA(close, timeperiod=long), index=close.index)
    dma = ma_short - ma_long
    ama = pd.Series(ta.MA(dma, timeperiod=m), index=close.index)
    return dma, ama
