from sqlalchemy import BigInteger, Column, Date, Numeric, String

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

    # 均线指标
    ma5 = Column(Numeric(10, 2), comment="5日均线")
    ma10 = Column(Numeric(10, 2), comment="10日均线")
    ma20 = Column(Numeric(10, 2), comment="20日均线")
    ma30 = Column(Numeric(10, 2), comment="30日均线")
    ma60 = Column(Numeric(10, 2), comment="60日均线")

    # MACD指标
    diff = Column(Numeric(10, 2), comment="DIFF线")
    dea = Column(Numeric(10, 2), comment="DEA线")
    macd = Column(Numeric(10, 2), comment="MACD柱")

    # KDJ指标
    k = Column(Numeric(10, 2), comment="K值")
    d = Column(Numeric(10, 2), comment="D值")
    j = Column(Numeric(10, 2), comment="J值")

    # RSI指标
    rsi6 = Column(Numeric(10, 2), comment="6日RSI")
    rsi12 = Column(Numeric(10, 2), comment="12日RSI")
    rsi24 = Column(Numeric(10, 2), comment="24日RSI")

    # 布林带指标
    boll_up = Column(Numeric(10, 2), comment="布林上轨")
    boll_mid = Column(Numeric(10, 2), comment="布林中轨")
    boll_down = Column(Numeric(10, 2), comment="布林下轨")

    # 成交量指标
    vma5 = Column(Numeric(20, 2), comment="5日成交量均线")
    vma10 = Column(Numeric(20, 2), comment="10日成交量均线")
    vma20 = Column(Numeric(20, 2), comment="20日成交量均线")

    # DMI指标
    pdi = Column(Numeric(10, 2), comment="PDI值")
    mdi = Column(Numeric(10, 2), comment="MDI值")
    adx = Column(Numeric(10, 2), comment="ADX值")
    adxr = Column(Numeric(10, 2), comment="ADXR值")

    # TRIX指标
    trix = Column(Numeric(10, 2), comment="TRIX值")
    matrix = Column(Numeric(10, 2), comment="MATRIX值")

    # CCI指标
    cci = Column(Numeric(10, 2), comment="CCI值")

    # ATR指标
    atr = Column(Numeric(10, 2), comment="ATR值")

    # CR指标
    cr = Column(Numeric(10, 2), comment="CR值")
    cr_ma1 = Column(Numeric(10, 2), comment="CR均线1")
    cr_ma2 = Column(Numeric(10, 2), comment="CR均线2")
    cr_ma3 = Column(Numeric(10, 2), comment="CR均线3")

    # ROC指标
    roc = Column(Numeric(10, 2), comment="ROC值")
    rocma = Column(Numeric(10, 2), comment="ROCMA值")

    # PSY指标
    psy = Column(Numeric(10, 2), comment="PSY值")
    psyma = Column(Numeric(10, 2), comment="PSYMA值")

    # DMA指标
    dma = Column(Numeric(10, 2), comment="DMA值")
    ama = Column(Numeric(10, 2), comment="AMA值")

    created_at = Column(BigInteger, default=get_now_millis())


class StockSignal(Base):
    """股票交易信号"""
    __tablename__ = "cn_stock_signal"
    
    id = Column(BigInteger, primary_key=True, index=True)
    code = Column(String(10), index=True, nullable=False, comment="股票代码")
    name = Column(String(100), nullable=False, comment="股票名称")
    trade_date = Column(Date, index=True, nullable=False, comment="交易日期")
    strategy = Column(String(50), nullable=False, comment="策略名称")
    signal_type = Column(String(10), nullable=False, comment="信号类型(buy/sell)")
    signal_desc = Column(String(200), comment="信号描述")
    created_at = Column(BigInteger, default=get_now_millis())
