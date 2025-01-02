import logging
from datetime import date
from typing import Optional

import akshare as ak
import pandas as pd

from app.core.database import Base
from app.core.service import BaseService
from app.models.stock import StockBlockTrade, StockDaily, StockInfo, StockLhb
from app.stock.datastore import StockDatastore
from app.tasks.stock_indicator_task import calculate_indicators_task
from app.utils.data_frame import df_process
from app.utils.date import SHORT_DATE_FORMAT, date_format, date_parse
from app.utils.stock import is_a_stock

logger = logging.getLogger(__name__)


class StockService(BaseService[StockDatastore, Base]):
    def __init__(self, datastore: StockDatastore):
        super().__init__(datastore)

    @classmethod
    def fetch_stock_info_list(cls) -> list[StockInfo]:
        stock_df = ak.stock_info_a_code_name()
        stock_df = stock_df.loc[stock_df["code"].apply(is_a_stock)]
        stock_df = stock_df.to_dict(orient="records")
        return [StockInfo(**a) for a in stock_df]

    def fetch_daily_data(self, start_date: date, end_date: Optional[date]) -> None:
        """抓取每日股票数据"""

        # 遍历获取每只股票数据
        for row in self.fetch_stock_info_list():
            code = row.code
            try:
                # 获取日线数据
                start_date_str = date_format(start_date, SHORT_DATE_FORMAT)
                df = ak.stock_zh_a_hist(
                    symbol=code,
                    period="daily",
                    start_date=start_date_str,
                    end_date=(
                        date_format(end_date, SHORT_DATE_FORMAT)
                        if end_date
                        else start_date_str
                    ),
                )
                if df.empty:
                    continue
                logger.info(f"获取股票{code}数据成功")
                # 转换数据
                stocks = []
                for _, data in df.iterrows():
                    trade_date = date_parse(data["日期"]).date()
                    stock = self.datastore.get_stock_daily(code, trade_date)
                    if stock:
                        continue
                    stocks.append(
                        StockDaily(
                            code=code,
                            name=row.name,
                            trade_date=trade_date,
                            open=data["开盘"],
                            high=data["最高"],
                            low=data["最低"],
                            close=data["收盘"],
                            volume=data["成交量"],
                            amount=data["成交额"],
                            turnover=data["换手率"],
                        )
                    )
                self.datastore.bulk_save(stocks)
                calculate_indicators_task.apply_async(
                    kwargs={"code": code, "start_date": date_format(start_date, SHORT_DATE_FORMAT)}
                )
            except Exception as e:
                logger.exception(f"获取股票{code}数据失败:{str(e)}")
                raise e

    def fetch_lhb_data(self, start_date: date, end_date: Optional[date]) -> None:
        """抓取龙虎榜数据"""
        try:
            data_str = date_format(start_date, SHORT_DATE_FORMAT)
            # 获取龙虎榜详情
            df = ak.stock_lhb_detail_em(
                start_date=data_str,
                end_date=(
                    date_format(end_date, SHORT_DATE_FORMAT) if end_date else data_str
                ),
            )
            if df.empty:
                return
            df = df_process(df, sort_column="上榜日", format_nan=True)
            # 转换数据
            stocks = []
            for _, data in df.iterrows():
                stocks.append(
                    StockLhb(
                        code=data["代码"],
                        name=data["名称"],
                        trade_date=date_parse(data["上榜日"]).date(),
                        reason=data["上榜原因"],
                        net_buy=data["龙虎榜净买额"],
                        buy_amount=data["龙虎榜买入额"],
                        sell_amount=data["龙虎榜卖出额"],
                        total_amount=data["龙虎榜成交额"],
                    )
                )
            self.datastore.bulk_save(stocks)
        except Exception as e:
            logger.exception(f"获取龙虎榜数据失败:{str(e)}")
            raise e

    def fetch_block_trade_data(
        self, start_date: date, end_date: Optional[date]
    ) -> None:
        """抓取大宗交易数据"""
        try:
            # 获取大宗交易数据
            start_date_str = date_format(start_date, SHORT_DATE_FORMAT)
            df = ak.stock_dzjy_mrmx(
                symbol="A股",
                start_date=start_date_str,
                end_date=(
                    date_format(end_date, SHORT_DATE_FORMAT)
                    if end_date
                    else start_date_str
                ),
            )
            if df.empty:
                return
            df = df_process(df, sort_column="交易日期", format_nan=True)

            # 转换数据
            stocks = []
            for _, data in df.iterrows():
                stocks.append(
                    StockBlockTrade(
                        code=data["证券代码"],
                        name=data["证券简称"],
                        trade_date=data["交易日期"],
                        price=data["成交价"],
                        volume=data["成交量"],
                        amount=data["成交额"],
                        buyer=data["买方营业部"],
                        seller=data["卖方营业部"],
                        premium=data["折溢率"],
                    )
                )
            self.datastore.bulk_save(stocks)
        except Exception as e:
            logger.exception(f"获取大宗交易数据失败:{str(e)}")
            raise e

    def get_history_with_indicators(
        self, code: str, start_date: Optional[str] = None
    ) -> pd.DataFrame:
        """获取带指标的历史数据"""
        try:
            # 获取基础数据和指标数据
            stocks = self.datastore.get_stock_history(code, start_date)
            indicators = self.datastore.get_indicator_history(code, start_date)

            if not stocks or not indicators:
                return pd.DataFrame()

            # 转换为DataFrame
            stock_data = []
            for stock in stocks:
                stock_data.append(
                    {
                        "code": stock.code,
                        "trade_date": stock.trade_date,
                        "open": float(stock.open),
                        "high": float(stock.high),
                        "low": float(stock.low),
                        "close": float(stock.close),
                        "volume": stock.volume,
                        "amount": stock.amount,
                    }
                )

            indicator_data = []
            for indicator in indicators:
                indicator_data.append(
                    {
                        "trade_date": indicator.trade_date,
                        "ma5": float(indicator.ma5),
                        "ma10": float(indicator.ma10),
                        "ma20": float(indicator.ma20),
                        "ma30": float(indicator.ma30),
                        "ma60": float(indicator.ma60),
                        "diff": float(indicator.diff),
                        "dea": float(indicator.dea),
                        "macd": float(indicator.macd),
                        "k": float(indicator.k),
                        "d": float(indicator.d),
                        "j": float(indicator.j),
                        "rsi6": float(indicator.rsi6),
                        "rsi12": float(indicator.rsi12),
                        "rsi24": float(indicator.rsi24),
                        "boll_up": float(indicator.boll_up),
                        "boll_mid": float(indicator.boll_mid),
                        "boll_down": float(indicator.boll_down),
                        "vma5": float(indicator.vma5),
                        "vma10": float(indicator.vma10),
                        "vma20": float(indicator.vma20),
                        "pdi": float(indicator.pdi),
                        "mdi": float(indicator.mdi),
                        "adx": float(indicator.adx),
                        "adxr": float(indicator.adxr),
                        "cci": float(indicator.cci),
                        # ... 其他指标
                    }
                )

            # 合并数据
            df_stock = pd.DataFrame(stock_data)
            df_indicator = pd.DataFrame(indicator_data)

            df = pd.merge(df_stock, df_indicator, on="trade_date")
            return df.sort_values("trade_date")

        except Exception as e:
            print(f"获取股票{code}历史数据失败: {str(e)}")
            return pd.DataFrame()
