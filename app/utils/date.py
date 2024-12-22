from typing import Optional

import arrow
from arrow import Arrow
from chinese_calendar import is_workday

DEFAULT_FORMAT = "YYYY-MM-DD HH:mm:ss"
SIMPLE_FORMAT = "YYYY-MM-DD"


def get_now_millis():
    return arrow.now().int_timestamp * 1000


def get_now():
    return arrow.now()


def format_date(date: Arrow, format_str: str = DEFAULT_FORMAT):
    return date.format(format_str)


def format_now(format_str: str = DEFAULT_FORMAT):
    return format_date(get_now(), format_str)


def get_last_trade_date(current_date: Optional[Arrow] = None) -> Arrow:
    """
    获取最后一个股票交易日

    规则：
    1. 如果当前时间是交易日且在15:00之前，返回上一个交易日
    2. 如果当前时间是交易日且在15:00之后，返回当前交易日
    3. 如果当前时间不是交易日，向前查找最近的交易日

    Args:
        current_date: 指定日期，如果为None则使用当前日期

    Returns:
        Arrow: 最后一个交易日的日期
    """
    if current_date is None:
        current_date = get_now()

    # 获取当前日期的日期部分
    current_date = current_date.floor("day")

    # 判断是否是交易日
    def is_trade_day(date: Arrow) -> bool:
        # 转换为datetime对象
        dt = date.datetime
        # 判断是否是工作日
        return is_workday(dt)

    # # 如果当前是交易日
    # if is_trade_day(current_date):
    #     current_time = get_now().time()
    #     market_close_time = time(15, 0)
    #
    #     # 如果当前时间在15:00之前，获取上一个交易日
    #     if current_time < market_close_time:
    #         current_date = current_date.shift(days=-1)

    # 向前查找最近的交易日
    while not is_trade_day(current_date):
        current_date = current_date.shift(days=-1)

    return current_date
