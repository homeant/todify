# 设置OpenAI API密钥

from app.stock.lhb import stock_lhb_detail_em, stock_lhb_jgmmtj_em


# 主流程
def test_longhubang():
    start_date = "20241216"
    end_date = "20241216"
    # 获取龙虎榜数据
    lhb_detail = stock_lhb_detail_em(start_date, end_date)
    lhb_detail = lhb_detail.drop(["上榜后10日"], axis=1)
    lhb_detail = lhb_detail[
        (lhb_detail["龙虎榜净买额"] > 10000000)  # 净买入金额 > 1000万元
        & (lhb_detail["换手率"] > 5)
        & (lhb_detail["换手率"] < 30)  # 换手率在10%-30%之间
        & (lhb_detail["净买额占总成交比"] > 5)  # 净买额占总成交额比 > 5%
        & (lhb_detail["成交额占总成交比"] > 10)  # 龙虎榜成交额占总成交额 > 10%
        & (
            lhb_detail["流通市值"] < 5000000000
        )  # 流通市值小于 500 亿（小盘股更容易炒作）
        & (lhb_detail["上榜后1日"] > 0)  # 上榜后1日股价有溢价
    ]
    print("\n" + lhb_detail.to_markdown(index=False, floatfmt=".2f"))

    # 获取机构每日买卖数据
    jgmm_data = stock_lhb_jgmmtj_em(start_date, end_date)
    jgmm_data = jgmm_data[
        (jgmm_data["机构买入净额"] > 10000000)  # 净买入金额 > 1000万元
        & (jgmm_data["换手率"] > 5)
        & (jgmm_data["换手率"] < 30)  # 换手率在10%-30%之间
        & (jgmm_data["机构净买额占总成交额比"] > 5)  # 净买额占总成交额比 > 5%
        & (
            jgmm_data["流通市值"] < 5000000000
        )  # 流通市值小于 500 亿（小盘股更容易炒作）
    ]
    # jgmm_data = set_float_format(jgmm_data)
    print("\n" + jgmm_data.to_markdown(index=False, floatfmt=".2f"))
    # llm = LLMFactory().get_instance("QwenClient")

    # messages = [
    #     "近五日龙虎榜数据：\n{}".format(lhb_detail.to_markdown(index=False)),
    #     "请根据以上数据，分析板块趋势，并给出总结"
    # ]

    # # 使用工具分析板块趋势
    # summary = llm.text_chat(messages)
    # analysis_result = llm.text_chat([
    #     "近五日机构买卖数据：\n{}".format(jgmm_data.to_markdown(index=False)),
    # ])
    # print(analysis_result)
