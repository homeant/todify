from typing import List

import pandas as pd

from app.core.database import SessionLocal
from app.stock.datastore import StockDatastore
from app.strategy._strategy import BaseStrategy


class BacktestEngine:
    """回测引擎"""

    def __init__(
        self,
        strategy: BaseStrategy,
        start_date: str,
        end_date: str,
        initial_capital: float = 1000000,
    ):
        self.strategy = strategy
        self.start_date = start_date
        self.end_date = end_date
        self.capital = initial_capital
        self.positions = {}  # 持仓
        self.trades = []  # 交易记录

        # 初始化数据存储
        self.db = SessionLocal()
        self.datastore = StockDatastore(self.db)

    def _get_daily_data(self, date: str) -> pd.DataFrame:
        """获取某日所有股票数据"""
        try:
            # 从数据库获取数据
            stocks = self.datastore.get_stocks_by_date(date)
            if not stocks:
                return pd.DataFrame()

            # 转换为DataFrame
            data = []
            for stock in stocks:
                data.append(
                    {
                        "code": stock.code,
                        "name": stock.name,
                        "open": float(stock.open),
                        "high": float(stock.high),
                        "low": float(stock.low),
                        "close": float(stock.close),
                        "volume": stock.volume,
                        "amount": stock.amount,
                        "turnover": float(stock.turnover),
                    }
                )

            return pd.DataFrame(data)

        except Exception as e:
            print(f"获取{date}数据失败: {str(e)}")
            return pd.DataFrame()

    def _buy_stock(self, code: str, date: str):
        """买入股票"""
        try:
            # 获取股票数据
            stock = self.datastore.get_stock_by_code_and_date(code, date)
            if not stock:
                return

            # 计算可买数量(假设每只股票使用10%资金)
            price = float(stock.close)
            amount = self.capital * 0.1
            volume = int(amount / price / 100) * 100  # 向下取整到100股

            if volume == 0:
                return

            # 记录交易
            cost = volume * price
            self.positions[code] = {"volume": volume, "cost": cost, "price": price}

            self.trades.append(
                {
                    "date": date,
                    "code": code,
                    "action": "buy",
                    "price": price,
                    "volume": volume,
                    "cost": cost,
                    "profit": 0,
                }
            )

            # 更新资金
            self.capital -= cost

        except Exception as e:
            print(f"买入股票{code}失败: {str(e)}")

    def _sell_stock(self, code: str, date: str):
        """卖出股票"""
        try:
            if code not in self.positions:
                return

            # 获取股票数据
            stock = self.datastore.get_stock_by_code_and_date(code, date)
            if not stock:
                return

            # 计算收益
            position = self.positions[code]
            price = float(stock.close)
            volume = position["volume"]
            revenue = volume * price
            profit = revenue - position["cost"]

            # 记录交易
            self.trades.append(
                {
                    "date": date,
                    "code": code,
                    "action": "sell",
                    "price": price,
                    "volume": volume,
                    "cost": -revenue,
                    "profit": profit,
                }
            )

            # 更新资金和持仓
            self.capital += revenue
            del self.positions[code]

        except Exception as e:
            print(f"卖出股票{code}失败: {str(e)}")

    def __del__(self):
        """析构函数,关闭数据库连接"""
        if hasattr(self, "db"):
            self.db.close()

    async def run(self) -> pd.DataFrame:
        """运行回测"""
        # 获取日期列表
        dates = pd.date_range(self.start_date, self.end_date)

        for date in dates:
            date_str = date.strftime("%Y%m%d")

            # 获取当日数据
            daily_data = await self._get_daily_data(date_str)
            if daily_data.empty:
                continue

            # 获取策略信号
            buy_list = await self.strategy.analyze(daily_data)

            # 执行交易
            await self._process_trades(date_str, buy_list)

        # 计算回测结果
        return self._calculate_results()

    async def _process_trades(self, date: str, buy_list: List[str]):
        """处理交易"""
        # 检查卖出信号
        for code in list(self.positions.keys()):
            if await self.strategy.get_sell_signal(code, date):
                await self._sell_stock(code, date)

        # 检查买入信号
        for code in buy_list:
            if code not in self.positions:
                await self._buy_stock(code, date)

    def _calculate_results(self) -> pd.DataFrame:
        """计算回测结果"""
        if not self.trades:
            return pd.DataFrame()

        # 转换交易记录为DataFrame
        df = pd.DataFrame(self.trades)

        # 计算收益率等指标
        df["returns"] = df["profit"] / self.capital
        df["cumulative_returns"] = (1 + df["returns"]).cumprod()

        return df
