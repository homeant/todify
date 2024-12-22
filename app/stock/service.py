import akshare as ak


def get_hot_rank(time: str):
    return ak.stock_hot_rank_wc(time)
