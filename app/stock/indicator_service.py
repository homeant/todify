import logging
from datetime import date
from typing import Optional

import pandas as pd

from app.core.service import BaseService
from app.models.stock import StockIndicator
from app.stock.datastore import StockDatastore
from app.utils.data_frame import df_process
from app.utils.date import date_parse
from app.utils.indicator import (
    calculate_boll,
    calculate_cci,
    calculate_dma,
    calculate_kdj,
    calculate_ma,
    calculate_macd,
    calculate_rsi,
    calculate_trix,
)

logger = logging.getLogger(__name__)


class StockIndicatorService(BaseService[StockDatastore, StockIndicator]):
    """指标计算服务"""

    def __init__(self, datastore: StockDatastore):
        super().__init__(datastore)

    def calculate_indicators(self, code: str, current_date: date) -> None:
        """计算股票技术指标"""
        logger.info(f"开始计算股票{code}的技术指标")
        old_indicator = self.datastore.get_indicator(code, current_date)
        if old_indicator:
            logger.info(f"股票{code}的技术指标已存在，跳过计算")
            return
        # 获取前120天的数据用于计算指标
        start_date = date_parse(current_date).shift(days=-120).format("YYYY-MM-DD")
        try:
            # 获取历史数据
            df = self._get_history_data(code, start_date)
            if df.empty:
                return

            # 计算均线 已验证
            ma_periods = [5, 10, 20, 30, 60]
            new_pd = pd.DataFrame()

            for period in ma_periods:
                new_pd[f"ma{period}"] = calculate_ma(df["close"], period)

            # 计算MACD 已验证
            diff, dea, macd = calculate_macd(df["close"])
            new_pd["diff"] = diff
            new_pd["dea"] = dea
            new_pd["macd"] = macd

            # 计算KDJ 已验证
            k, d, j = calculate_kdj(df["high"], df["low"], df["close"])
            new_pd["k"] = k
            new_pd["d"] = d
            new_pd["j"] = j

            # 计算RSI
            new_pd["rsi6"] = calculate_rsi(df["close"], 6)  # 已验证
            new_pd["rsi12"] = calculate_rsi(df["close"], 12)
            new_pd["rsi24"] = calculate_rsi(df["close"], 24)

            # 计算布林带 已验证
            up, mid, down = calculate_boll(df["close"])
            new_pd["boll_up"] = up
            new_pd["boll_mid"] = mid
            new_pd["boll_down"] = down

            # 计算成交量均线 已验证
            for period in [5, 10, 20]:
                new_pd[f"vma{period}"] = calculate_ma(df["volume"], period)

            # 计算DMI
            # pdi, mdi, adx, adxr = calculate_dmi(df["high"], df["low"], df["close"])
            # new_pd["pdi"] = pdi
            # new_pd["mdi"] = mdi
            # new_pd["adx"] = adx
            # new_pd["adxr"] = adxr

            # 计算TRIX
            trix, matrix = calculate_trix(df["close"])
            new_pd["trix"] = trix
            new_pd["matrix"] = matrix

            # 计算CCI 已验证
            new_pd["cci"] = calculate_cci(df["high"], df["low"], df["close"])

            # 计算DMA 已验证
            dma, ama = calculate_dma(df["close"])
            new_pd["dma"] = dma
            new_pd["ama"] = ama

            new_pd = df_process(new_pd, format_nan=True)

            # 只获取指定日期的数据
            row = new_pd.loc[pd.to_datetime(current_date)]

            if pd.isna(row["ma60"]):  # 数据不足则跳过
                return
            # 创建单个指标记录
            indicator = StockIndicator(
                code=code,
                trade_date=current_date,
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
                # pdi=row["pdi"],
                # mdi=row["mdi"],
                # adx=row["adx"],
                # adxr=row["adxr"],
                trix=row["trix"],
                # matrix=row["matrix"],
                cci=row["cci"],
                dma=row["dma"],
                ama=row["ama"],
            )
            # 保存单个指标记录
            self.datastore.upsert(indicator)

        except Exception as e:
            logger.exception(f"计算股票{code}指标失败: {str(e)}")

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
