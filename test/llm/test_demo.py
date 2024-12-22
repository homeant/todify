import akshare as ak
import matplotlib.pyplot as plt
import pandas as pd

from app.llm.llm_factory import LLMFactory


# 获取股票历史数据
def get_stock_data(stock_code: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    使用 akshare 获取股票历史数据
    """
    stock_data = ak.stock_zh_a_hist(
        symbol=stock_code,
        period="daily",
        start_date=start_date,
        end_date=end_date,
        adjust="qfq",
    )
    stock_data.rename(
        columns={
            "日期": "Date",
            "开盘": "Open",
            "收盘": "Close",
            "最高": "High",
            "最低": "Low",
            "成交量": "Volume",
            "成交额": "Amount",
        },
        inplace=True,
    )
    stock_data["Date"] = pd.to_datetime(stock_data["Date"])
    return stock_data


# 可视化股票数据
def visualize_stock_data(stock_data: pd.DataFrame):
    """
    绘制股票收盘价走势图
    """
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data["Date"], stock_data["Close"], label="Close Price")
    plt.title("Stock Price Trend")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.legend()
    plt.grid()
    plt.show()


# 数据摘要生成
def summarize_data(stock_data: pd.DataFrame) -> str:
    """
    简要统计数据的基本情况
    """
    summary = {
        "平均收盘价": stock_data["Close"].mean(),
        "最高收盘价": stock_data["Close"].max(),
        "最低收盘价": stock_data["Close"].min(),
        "总成交量": stock_data["Volume"].sum(),
    }
    return f"""
    平均收盘价: {summary['平均收盘价']:.2f}
    最高收盘价: {summary['最高收盘价']:.2f}
    最低收盘价: {summary['最低收盘价']:.2f}
    总成交量: {summary['总成交量']:.2f}
    """


# 主函数
def test_demo():
    # 输入参数
    stock_code = "600797"  # 示例：平安银行（需改为具体股票代码）
    start_date = "20241201"
    end_date = "20241214"

    # 获取股票数据
    stock_data = get_stock_data(stock_code, start_date, end_date)

    # 可视化股票数据
    visualize_stock_data(stock_data)

    # 数据摘要
    data_summary = summarize_data(stock_data)
    print("数据摘要：")
    print(data_summary)

    # 使用LangChain进行分析
    langchain_prompt = f"""
    数据如下：
    {data_summary}
    根据上述数据，请分析股票的近期趋势并预测未来1个月可能的走势。
    请结合成交量和价格变化进行分析。
    """
    llm = LLMFactory().get_instance("SiliconFlowClient")

    analysis_result = llm.text_chat(langchain_prompt)
    print("\nLangChain分析结果：")
    print(analysis_result)
