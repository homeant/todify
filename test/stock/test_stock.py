import akshare as ak


def test_hot_rank():
    time_str = "20241206"
    hot_rank_value = ak.stock_hot_rank_wc(time_str).to_markdown()
    print(hot_rank_value)
