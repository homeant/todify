from typing import Optional

import arrow
import pandas as pd

from app.core.service import BaseService
from app.models.stock import StockIndicator
from app.stock.datastore import StockDatastore
from app.utils.indicator import (
    calculate_atr,
    calculate_boll,
    calculate_cci,
    calculate_cr,
    calculate_dma,
    calculate_dmi,
    calculate_kdj,
    calculate_ma,
    calculate_macd,
    calculate_psy,
    calculate_roc,
    calculate_rsi,
    calculate_trix,
)


class StockIndicatorService(BaseService[StockDatastore, StockIndicator]):
    """指标计算服务"""

    def __init__(self, datastore: StockDatastore):
        super().__init__(datastore)

    def calculate_indicators(self, code: str, date: str) -> None:
        """计算股票技术指标"""
        # 获取前60天
        start_date = arrow.get(date).shift(days=-90).format("YYYY-MM-DD")
        try:
            # 获取历史数据
            df = self._get_history_data(code, start_date)
            if df.empty:
                return

            # 计算各项指标
            indicators = []

            # 计算均线
            ma_periods = [5, 10, 20, 30, 60]
            for period in ma_periods:
                df[f"ma{period}"] = calculate_ma(df["close"], period)

            # 计算MACD
            diff, dea, macd = calculate_macd(df["close"])
            df["diff"] = diff
            df["dea"] = dea
            df["macd"] = macd

            # 计算KDJ
            k, d, j = calculate_kdj(df["high"], df["low"], df["close"])
            df["k"] = k
            df["d"] = d
            df["j"] = j

            # 计算RSI
            df["rsi6"] = calculate_rsi(df["close"], 6)
            df["rsi12"] = calculate_rsi(df["close"], 12)
            df["rsi24"] = calculate_rsi(df["close"], 24)

            # 计算布林带
            up, mid, down = calculate_boll(df["close"])
            df["boll_up"] = up
            df["boll_mid"] = mid
            df["boll_down"] = down

            # 计算成交量均线
            for period in [5, 10, 20]:
                df[f"vma{period}"] = calculate_ma(df["volume"], period)

            # 计算DMI
            pdi, mdi, adx, adxr = calculate_dmi(df["high"], df["low"], df["close"])
            df["pdi"] = pdi
            df["mdi"] = mdi
            df["adx"] = adx
            df["adxr"] = adxr

            # 计算TRIX
            trix, matrix = calculate_trix(df["close"])
            df["trix"] = trix
            df["matrix"] = matrix

            # 计算CCI
            df["cci"] = calculate_cci(df["high"], df["low"], df["close"])

            # 计算ATR
            df["atr"] = calculate_atr(df["high"], df["low"], df["close"])

            # 计算CR
            cr, cr_ma1, cr_ma2, cr_ma3 = calculate_cr(df["high"], df["low"])
            df["cr"] = cr
            df["cr_ma1"] = cr_ma1
            df["cr_ma2"] = cr_ma2
            df["cr_ma3"] = cr_ma3

            # 计算ROC
            roc, rocma = calculate_roc(df["close"])
            df["roc"] = roc
            df["rocma"] = rocma

            # 计算PSY
            psy, psyma = calculate_psy(df["close"])
            df["psy"] = psy
            df["psyma"] = psyma

            # 计算DMA
            dma, ama = calculate_dma(df["close"])
            df["dma"] = dma
            df["ama"] = ama

            # 转换为指标记录
            for _, row in df.iterrows():
                if pd.isna(row["ma60"]):  # 跳过数据不足的记录
                    continue

                indicator = StockIndicator(
                    code=code,
                    trade_date=arrow.get(date).date(),
                    ma5=row["ma5"],
                    ma10=row["ma10"],
                    ma20=row["ma20"],
                    ma30=row["ma30"],
                    ma60=row["ma60"],
                    diff=row["diff"],
                    dea=row["dea"],
                    macd=row["macd"],
                    k=row["k"],
                    d=row["d"],
                    j=row["j"],
                    rsi6=row["rsi6"],
                    rsi12=row["rsi12"],
                    rsi24=row["rsi24"],
                    boll_up=row["boll_up"],
                    boll_mid=row["boll_mid"],
                    boll_down=row["boll_down"],
                    vma5=row["vma5"],
                    vma10=row["vma10"],
                    vma20=row["vma20"],
                    pdi=row["pdi"],
                    mdi=row["mdi"],
                    adx=row["adx"],
                    adxr=row["adxr"],
                    trix=row["trix"],
                    matrix=row["matrix"],
                    cci=row["cci"],
                    atr=row["atr"],
                    cr=row["cr"],
                    cr_ma1=row["cr_ma1"],
                    cr_ma2=row["cr_ma2"],
                    cr_ma3=row["cr_ma3"],
                    roc=row["roc"],
                    rocma=row["rocma"],
                    psy=row["psy"],
                    psyma=row["psyma"],
                    dma=row["dma"],
                    ama=row["ama"],
                )
                indicators.append(indicator)

            # 批量保存
            if indicators:
                self.datastore.bulk_save(indicators)

        except Exception as e:
            print(f"计算股票{code}指标失败: {str(e)}")

    def _get_history_data(
        self, code: str, start_date: Optional[str] = None
    ) -> pd.DataFrame:
        """获取历史数据"""
        stocks = self.datastore.get_stock_history(code, start_date)
        if not stocks:
            return pd.DataFrame()

        # 转换为DataFrame
        data = []
        for stock in stocks:
            data.append(
                {
                    "code": stock.code,
                    "open": float(stock.open),
                    "high": float(stock.high),
                    "low": float(stock.low),
                    "close": float(stock.close),
                    "volume": stock.volume,
                    "amount": stock.amount,
                }
            )

        df = pd.DataFrame(data)
        df.index = pd.to_datetime([stock.trade_date for stock in stocks])
        return df.sort_index()
