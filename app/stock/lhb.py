from typing import Literal

import akshare as ak
from langchain_core.tools import tool


@tool
def stock_lhb_hyyyb_em(start_date: str = "20220324", end_date: str = "20220324"):
    """
    龙虎榜单-每日活跃营业部
    :param start_date:
    :param end_date:
    :return:
    """
    return ak.stock_lhb_hyyyb_em(start_date, end_date).to_markdown(floatfmt=".2f")


@tool
def stock_lhb_jgstatistic_em(period: Literal["近一月", "近三月", "近六月", "近一年"]):
    """
    龙虎榜单-机构席位追踪
    :param period:
    :return:
    """
    return ak.stock_lhb_jgstatistic_em(period).to_markdown(floatfmt=".2f")


@tool
def stock_lhb_stock_statistic_em(
    period: Literal["近一月", "近三月", "近六月", "近一年"]
):
    """
    龙虎榜单-个股上榜统计
    :param period:
    :return:
    """
    return ak.stock_lhb_stock_statistic_em(period).to_markdown(floatfmt=".2f")


@tool
def stock_lhb_detail_em(start_date: str = "20230403", end_date: str = "20230417"):
    """
    龙虎榜单-龙虎榜详情
    :param start_date:
    :param end_date:
    :return:
    """
    df = ak.stock_lhb_detail_em(start_date, end_date)
    return df.drop(["序号"], axis=1).to_markdown(floatfmt=".2f")


@tool
def stock_lhb_jgmmtj_em(start_date: str = "20240417", end_date: str = "20240430"):
    """
    龙虎榜单-机构买卖每日统计
    :param start_date:
    :param end_date:
    :return:
    """
    return ak.stock_lhb_jgmmtj_em(start_date, end_date).to_markdown(floatfmt=".2f")
