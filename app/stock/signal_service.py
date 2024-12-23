from typing import List, Optional
from datetime import datetime
from app.core.service import BaseService
from app.models.stock import StockSignal
from app.stock.datastore import StockDatastore
from app.strategy.factory import StrategyFactory
from app.utils.telegram import TelegramBot
import pandas as pd

class SignalService(BaseService[StockDatastore, StockSignal]):
    """交易信号服务"""
    
    def __init__(self, datastore: StockDatastore):
        super().__init__(datastore)
        self.factory = StrategyFactory()
        self.telegram = TelegramBot()
        
    async def generate_signals(self, date: str) -> None:
        """生成交易信号"""
        try:
            # 获取所有策略
            strategies = self.factory.list_strategies()
            
            # 获取当日数据
            stocks = await self.datastore.get_stocks_by_date(date)
            if not stocks:
                return
                
            # 转换为DataFrame
            stock_data = []
            for stock in stocks:
                stock_data.append({
                    'code': stock.code,
                    'name': stock.name,
                    'trade_date': stock.trade_date,
                    'open': float(stock.open),
                    'high': float(stock.high),
                    'low': float(stock.low),
                    'close': float(stock.close),
                    'volume': stock.volume,
                    'amount': stock.amount
                })
            
            # 获取指标数据
            indicators = await self.datastore.get_indicators_by_date(date)
            indicator_data = []
            for indicator in indicators:
                indicator_data.append({
                    'trade_date': indicator.trade_date,
                    'ma5': float(indicator.ma5),
                    # ... 其他指标
                })
            
            # 合并数据
            df_stock = pd.DataFrame(stock_data)
            df_indicator = pd.DataFrame(indicator_data)
            df = pd.merge(df_stock, df_indicator, on='trade_date')
            
            # 遍历策略生成信号
            signals = []
            for strategy_info in strategies:
                strategy = self.factory.get_strategy(strategy_info['name'])
                
                # 获取买入信号
                buy_list = await strategy.analyze(df)
                for code in buy_list:
                    stock = next(s for s in stocks if s.code == code)
                    signal = StockSignal(
                        code=code,
                        name=stock.name,
                        trade_date=datetime.strptime(date, '%Y%m%d').date(),
                        strategy=strategy.name,
                        signal_type='buy',
                        signal_desc=f"{strategy.name}买入信号"
                    )
                    signals.append(signal)
                
                # 获取卖出信号
                for stock in stocks:
                    if await strategy.get_sell_signal(stock.code, date):
                        signal = StockSignal(
                            code=stock.code,
                            name=stock.name,
                            trade_date=datetime.strptime(date, '%Y%m%d').date(),
                            strategy=strategy.name,
                            signal_type='sell',
                            signal_desc=f"{strategy.name}卖出信号"
                        )
                        signals.append(signal)
            
            # 批量保存信号
            if signals:
                await self.datastore.bulk_save(signals)
                
                # 推送到Telegram
                await self.telegram.send_signals(signals, date)
                
        except Exception as e:
            print(f"生成{date}交易信号失败: {str(e)}") 