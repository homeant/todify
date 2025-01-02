import numpy as np


def get_ma_support_price(ma_short, current_price):
    """
    根据均线计算支撑位
    """
    return ma_short if current_price > ma_short else None


def get_ma_resistance_price(ma_long, current_price):
    """
    根据均线计算压力位
    """
    return ma_long if current_price < ma_long else None

def get_recent_low_df(df, days=20):
    """
    使用 DataFrame 计算最近低点
    :param df: 包含价格数据的 DataFrame（需要有 'low' 列）
    :param days: 时间窗口长度
    :return: 最近的最低点和对应日期
    """
    if len(df) < days:
        raise ValueError("数据不足以计算最近低点")
    recent_data = df[-days:]
    recent_low = recent_data['low'].min()
    recent_date = recent_data[recent_data['low'] == recent_low].index[0]
    return recent_date, recent_low

# 600开头的股票是上证A股，属于大盘股
# 600开头的股票是上证A股，属于大盘股，其中6006开头的股票是最早上市的股票，
# 6016开头的股票为大盘蓝筹股；900开头的股票是上证B股；
# 000开头的股票是深证A股，001、002开头的股票也都属于深证A股，
# 其中002开头的股票是深证A股中小企业股票；
# 200开头的股票是深证B股；
# 300开头的股票是创业板股票；400开头的股票是三板市场股票。
def is_a_stock(code):
    # 上证A股  # 深证A股
    return code.startswith(('600', '601', '000', '001', '002'))


# 过滤掉 st 股票。
def is_not_st(name):
    return not name.startswith(('*ST', 'ST'))


# 过滤价格，如果没有基本上是退市了。
def is_open(latest_price):
    return not np.isnan(latest_price)
