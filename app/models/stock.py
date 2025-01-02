import pandas as pd
from sqlalchemy import BigInteger, Boolean, Column, Date, Numeric, String

from app.core.database import Base
from app.utils.date import get_now_millis


class StockDaily(Base):
    """每日股票数据"""

    __tablename__ = "cn_stock_daily"

    id = Column(BigInteger, primary_key=True, index=True)
    code = Column(String(10), index=True, nullable=False, comment="股票代码")
    name = Column(String(100), nullable=False, comment="股票名称")
    trade_date = Column(Date, index=True, nullable=False, comment="交易日期")
    open = Column(Numeric(10, 2), comment="开盘价")
    high = Column(Numeric(10, 2), comment="最高价")
    low = Column(Numeric(10, 2), comment="最低价")
    close = Column(Numeric(10, 2), comment="收盘价")
    volume = Column(BigInteger, comment="成交量")
    amount = Column(BigInteger, comment="成交额")
    turnover = Column(Numeric(10, 2), comment="换手率")
    created_at = Column(BigInteger, default=get_now_millis())

    def to_df(self):
        data = [
            {
                "code": self.code,
                "name": self.name,
                "open": float(self.open),
                "high": float(self.high),
                "low": float(self.low),
                "close": float(self.close),
                "volume": self.volume,
                "amount": self.amount,
            }
        ]

        df = pd.DataFrame(data)
        df.index = pd.to_datetime([self.trade_date])
        return df


class StockLhb(Base):
    """龙虎榜数据"""

    __tablename__ = "cn_stock_lhb"

    id = Column(BigInteger, primary_key=True, index=True)
    code = Column(String(10), index=True, nullable=False, comment="股票代码")
    name = Column(String(100), nullable=False, comment="股票名称")
    trade_date = Column(Date, index=True, nullable=False, comment="交易日期")
    reason = Column(String(200), comment="上榜原因")
    net_buy = Column(Numeric(20, 2), comment="净买入额")
    buy_amount = Column(Numeric(20, 2), comment="买入额")
    sell_amount = Column(Numeric(20, 2), comment="卖出额")
    total_amount = Column(Numeric(20, 2), comment="成交额")
    created_at = Column(BigInteger, default=get_now_millis())


class StockBlockTrade(Base):
    """大宗交易数据"""

    __tablename__ = "cn_stock_block_trade"

    id = Column(BigInteger, primary_key=True, index=True)
    code = Column(String(10), index=True, nullable=False, comment="股票代码")
    name = Column(String(100), nullable=False, comment="股票名称")
    trade_date = Column(Date, index=True, nullable=False, comment="交易日期")
    price = Column(Numeric(10, 2), comment="成交价")
    volume = Column(BigInteger, comment="成交量(手)")
    amount = Column(Numeric(20, 2), comment="成交额")
    buyer = Column(String(100), comment="买方营业部")
    seller = Column(String(100), comment="卖方营业部")
    premium = Column(Numeric(10, 2), comment="溢价率")
    created_at = Column(BigInteger, default=get_now_millis())


class StockIndicator(Base):
    """股票技术指标"""

    __tablename__ = "cn_stock_indicator"

    id = Column(BigInteger, primary_key=True, index=True)
    code = Column(String(10), index=True, nullable=False, comment="股票代码")
    trade_date = Column(Date, index=True, nullable=False, comment="交易日期")
    name = Column(String(50), nullable=False, comment="股票名称")
    # 均线指标 已验证
    ma5 = Column(Numeric(10, 2), comment="5日均线")
    ma10 = Column(Numeric(10, 2), comment="10日均线")
    ma20 = Column(Numeric(10, 2), comment="20日均线")
    ma30 = Column(Numeric(10, 2), comment="30日均线")
    ma60 = Column(Numeric(10, 2), comment="60日均线")

    # MACD指标 已验证
    diff = Column(Numeric(10, 2), comment="DIFF线")
    dea = Column(Numeric(10, 2), comment="DEA线")
    macd = Column(Numeric(10, 2), comment="MACD柱")

    # KDJ指标 已验证
    k = Column(Numeric(10, 2), comment="K值")
    d = Column(Numeric(10, 2), comment="D值")
    j = Column(Numeric(10, 2), comment="J值")

    # RSI指标
    rsi6 = Column(Numeric(10, 2), comment="6日RSI")  # 已验证
    rsi12 = Column(Numeric(10, 2), comment="12日RSI")
    rsi24 = Column(Numeric(10, 2), comment="24日RSI")

    # 布林带指标 已验证
    boll_up = Column(Numeric(10, 2), comment="布林上轨")
    boll_mid = Column(Numeric(10, 2), comment="布林中轨")
    boll_down = Column(Numeric(10, 2), comment="布林下轨")

    # 成交量指标 已验证
    vma5 = Column(Numeric(20, 2), comment="5日成交量均线")
    vma10 = Column(Numeric(20, 2), comment="10日成交量均线")
    vma20 = Column(Numeric(20, 2), comment="20日成交量均线")

    # DMI指标
    pdi = Column(Numeric(10, 2), comment="PDI值")
    mdi = Column(Numeric(10, 2), comment="MDI值")
    adx = Column(Numeric(10, 2), comment="ADX值")
    adxr = Column(Numeric(10, 2), comment="ADXR值")

    # TRIX指标
    trix = Column(Numeric(10, 2), comment="TRIX值")  # 已验证
    matrix = Column(Numeric(10, 2), comment="MATRIX值")

    # CCI指标 已验证
    cci = Column(Numeric(10, 2), comment="CCI值")

    # DMA指标 已验证
    dma = Column(Numeric(10, 2), comment="DMA值")
    ama = Column(Numeric(10, 2), comment="AMA值")

    created_at = Column(BigInteger, default=get_now_millis())


class StockSignal(Base):
    """股票技术指标信号"""

    __tablename__ = "cn_stock_signal"

    id = Column(BigInteger, primary_key=True, index=True)
    code = Column(String(10), index=True, nullable=False, comment="股票代码")
    name = Column(String(100), nullable=False, comment="股票名称")
    trade_date = Column(Date, index=True, nullable=False, comment="交易日期")

    # MACD信号
    macd_golden_cross = Column(Boolean, default=False, comment="MACD金叉")
    macd_dead_cross = Column(Boolean, default=False, comment="MACD死叉")

    # KDJ信号
    kdj_golden_cross = Column(Boolean, default=False, comment="KDJ金叉")
    kdj_dead_cross = Column(Boolean, default=False, comment="KDJ死叉")
    kdj_oversold = Column(Boolean, default=False, comment="KDJ超卖")
    kdj_overbought = Column(Boolean, default=False, comment="KDJ超买")

    # RSI信号
    rsi_oversold = Column(Boolean, default=False, comment="RSI超卖")
    rsi_overbought = Column(Boolean, default=False, comment="RSI超买")

    # 布林带信号
    boll_break_up = Column(Boolean, default=False, comment="突破布林上轨")
    boll_break_down = Column(Boolean, default=False, comment="突破布林下轨")

    # 均线信号
    ma_golden_cross = Column(
        Boolean, default=False, comment="均线金叉(5日线上穿20日线)"
    )
    ma_dead_cross = Column(Boolean, default=False, comment="均线死叉(5日线下穿20日线)")

    price_rebound = Column(Boolean, default=False, comment="价格回升")

    # AI分析结果
    ai_analysis = Column(String(1000), comment="AI分析结果")
    ai_score = Column(Numeric(5, 2), comment="AI评分(0-100)")

    created_at = Column(BigInteger, default=get_now_millis())
