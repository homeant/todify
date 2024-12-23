import pandas as pd


def calculate_ma(data: pd.Series, n: int) -> pd.Series:
    """计算移动平均线"""
    return data.rolling(window=n).mean()


def calculate_macd(
    close: pd.Series,
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9,
) -> tuple:
    """计算MACD指标"""
    ema_fast = close.ewm(span=fast_period, adjust=False).mean()
    ema_slow = close.ewm(span=slow_period, adjust=False).mean()
    diff = ema_fast - ema_slow
    dea = diff.ewm(span=signal_period, adjust=False).mean()
    macd = 2 * (diff - dea)
    return diff, dea, macd


def calculate_kdj(
    high: pd.Series, low: pd.Series, close: pd.Series, n: int = 9
) -> tuple:
    """计算KDJ指标"""
    rsv = (
        (close - low.rolling(n).min())
        / (high.rolling(n).max() - low.rolling(n).min())
        * 100
    )
    k = rsv.ewm(com=2).mean()
    d = k.ewm(com=2).mean()
    j = 3 * k - 2 * d
    return k, d, j


def calculate_rsi(close: pd.Series, n: int = 14) -> pd.Series:
    """计算RSI指标"""
    diff = close.diff()
    up = diff.clip(lower=0)
    down = -diff.clip(upper=0)
    ma_up = up.ewm(com=n - 1, adjust=False).mean()
    ma_down = down.ewm(com=n - 1, adjust=False).mean()
    rsi = ma_up / (ma_up + ma_down) * 100
    return rsi


def calculate_boll(close: pd.Series, n: int = 20, k: float = 2) -> tuple:
    """计算布林带"""
    mid = close.rolling(window=n).mean()
    std = close.rolling(window=n).std()
    up = mid + k * std
    down = mid - k * std
    return up, mid, down


def calculate_dmi(
    high: pd.Series, low: pd.Series, close: pd.Series, n: int = 14
) -> tuple:
    """计算DMI指标"""
    tr = pd.DataFrame()
    tr["h-l"] = high - low
    tr["h-c"] = abs(high - close.shift(1))
    tr["l-c"] = abs(low - close.shift(1))
    tr = tr.max(axis=1)

    hd = high - high.shift(1)
    ld = low.shift(1) - low

    pdm = pd.Series(0, index=high.index)
    pdm[hd > ld] = hd[hd > ld]
    pdm[hd <= ld] = 0

    mdm = pd.Series(0, index=high.index)
    mdm[ld > hd] = ld[ld > hd]
    mdm[ld <= hd] = 0

    tr14 = tr.rolling(n).sum()
    pdi14 = pdm.rolling(n).sum() / tr14 * 100
    mdi14 = mdm.rolling(n).sum() / tr14 * 100

    adx = abs(pdi14 - mdi14) / (pdi14 + mdi14) * 100
    adx = adx.rolling(n).mean()

    adxr = (adx + adx.shift(n)) / 2

    return pdi14, mdi14, adx, adxr


def calculate_trix(close: pd.Series, n: int = 12, m: int = 9) -> tuple:
    """计算TRIX指标"""
    tr = close.ewm(span=n, adjust=False).mean()
    tr = tr.ewm(span=n, adjust=False).mean()
    tr = tr.ewm(span=n, adjust=False).mean()

    trix = (tr - tr.shift(1)) / tr.shift(1) * 100
    matrix = trix.rolling(m).mean()

    return trix, matrix


def calculate_cci(
    high: pd.Series, low: pd.Series, close: pd.Series, n: int = 14
) -> pd.Series:
    """计算CCI指标"""
    tp = (high + low + close) / 3
    ma = tp.rolling(n).mean()
    md = abs(tp - ma).rolling(n).mean()
    cci = (tp - ma) / (md * 0.015)
    return cci


def calculate_atr(
    high: pd.Series, low: pd.Series, close: pd.Series, n: int = 14
) -> pd.Series:
    """计算ATR指标"""
    tr = pd.DataFrame()
    tr["h-l"] = high - low
    tr["h-c"] = abs(high - close.shift(1))
    tr["l-c"] = abs(low - close.shift(1))
    tr = tr.max(axis=1)
    atr = tr.rolling(n).mean()
    return atr


def calculate_cr(high: pd.Series, low: pd.Series, n: int = 26) -> tuple:
    """计算CR指标"""
    mid = (high + low) / 2
    p1 = pd.Series(0, index=high.index)
    p2 = pd.Series(0, index=high.index)

    p1[high > mid.shift(1)] = (
        high[high > mid.shift(1)] - mid.shift(1)[high > mid.shift(1)]
    )
    p2[low < mid.shift(1)] = mid.shift(1)[low < mid.shift(1)] - low[low < mid.shift(1)]

    cr = p1.rolling(n).sum() / p2.rolling(n).sum() * 100
    cr_ma1 = cr.rolling(5).mean()
    cr_ma2 = cr.rolling(10).mean()
    cr_ma3 = cr.rolling(20).mean()

    return cr, cr_ma1, cr_ma2, cr_ma3


def calculate_roc(close: pd.Series, n: int = 12, m: int = 6) -> tuple:
    """计算ROC指标"""
    roc = (close - close.shift(n)) / close.shift(n) * 100
    rocma = roc.rolling(m).mean()
    return roc, rocma


def calculate_psy(close: pd.Series, n: int = 12, m: int = 6) -> tuple:
    """计算PSY指标"""
    diff = close - close.shift(1)
    psy = diff[diff > 0].rolling(n).count() / n * 100
    psyma = psy.rolling(m).mean()
    return psy, psyma


def calculate_dma(
    close: pd.Series, short: int = 10, long: int = 50, m: int = 10
) -> tuple:
    """计算DMA指标"""
    ma_short = close.rolling(short).mean()
    ma_long = close.rolling(long).mean()
    dma = ma_short - ma_long
    ama = dma.rolling(m).mean()
    return dma, ama
