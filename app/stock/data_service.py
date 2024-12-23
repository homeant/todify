from datetime import datetime
from typing import Optional

import akshare as ak
import pandas as pd

from app.core.service import BaseService
from app.models.stock import StockBlockTrade, StockDaily, StockLhb
from app.stock.datastore import StockDatastore


class StockDataService(BaseService[StockDatastore, StockDaily]):
    def __init__(self, datastore: StockDatastore):
        super().__init__(datastore)

    async def fetch_daily_data(self, date: Optional[str] = None) -> None:
        """抓取每日股票数据"""
        # 获取股票列表
        stock_info = ak.stock_info_a_code_name()

        # 遍历获取每只股票数据
        for _, row in stock_info.iterrows():
            try:
                code = row["code"]
                name = row["name"]

                # 获取日线数据
                df = ak.stock_zh_a_hist(
                    symbol=code, period="daily", start_date=date, end_date=date
                )

                if df.empty:
                    continue

                # 转换数据
                for _, data in df.iterrows():
                    stock = StockDaily(
                        code=code,
                        name=name,
                        trade_date=datetime.strptime(date, "%Y%m%d").date(),
                        open=data["开盘"],
                        high=data["最高"],
                        low=data["最低"],
                        close=data["收盘"],
                        volume=data["成交量"],
                        amount=data["成交额"],
                        turnover=data["换手率"],
                    )
                    # 保存数据
                    await self.datastore.upsert(stock)

            except Exception as e:
                print(f"获取股票{code}数据失败:{str(e)}")

    async def fetch_lhb_data(self, date: Optional[str] = None) -> None:
        """抓取龙虎榜数据"""
        try:
            # 获取龙虎榜详情
            df = ak.stock_lhb_detail_em(start_date=date, end_date=date)
            if df.empty:
                return

            # 转换数据
            for _, data in df.iterrows():
                lhb = StockLhb(
                    code=data["代码"],
                    name=data["名称"],
                    trade_date=datetime.strptime(date, "%Y%m%d").date(),
                    reason=data["上榜原因"],
                    net_buy=data["净买额"] if "净买额" in data else 0,
                    buy_amount=data["买入额"] if "买入额" in data else 0,
                    sell_amount=data["卖出额"] if "卖出额" in data else 0,
                    total_amount=data["���交额"] if "成交额" in data else 0,
                )
                await self.datastore.upsert(lhb)

        except Exception as e:
            print(f"获取龙虎榜数据失败:{str(e)}")

    async def fetch_block_trade_data(self, date: Optional[str] = None) -> None:
        """抓取大宗交易数据"""
        try:
            # 获取大宗交易数据
            df = ak.stock_dzjy_mrtj(start_date=date, end_date=date)
            if df.empty:
                return

            # 转换数据
            for _, data in df.iterrows():
                block_trade = StockBlockTrade(
                    code=data["证券代码"],
                    name=data["证券简称"],
                    trade_date=datetime.strptime(date, "%Y%m%d").date(),
                    price=data["成交价格"],
                    volume=data["成交量"],
                    amount=data["成交金额"],
                    buyer=data["买方营业部"],
                    seller=data["卖方营业部"],
                    premium=data["溢价率"],
                )
                await self.datastore.upsert(block_trade)

        except Exception as e:
            print(f"获取大宗交易数据失败:{str(e)}")

    async def get_history_with_indicators(
        self, code: str, start_date: Optional[str] = None
    ) -> pd.DataFrame:
        """获取带指标的历史数据"""
        try:
            # 获取基础数据和指标数据
            stocks = await self.datastore.get_stock_history(code, start_date)
            indicators = await self.datastore.get_indicator_history(code, start_date)

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
