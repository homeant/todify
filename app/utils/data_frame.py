from typing import Optional

import pandas as pd
import numpy as np

def df_process(df: pd.DataFrame, format_nan: Optional[bool] = False, sort_column: Optional[str] = None, ascending: bool = True) -> pd.DataFrame:
    if format_nan:
        df = df.apply(lambda col: col.fillna(0) if col.dtype in [np.float64, np.int64] else col)
    if sort_column:
        df = df.sort_values(by=sort_column, ascending=ascending)
    return df