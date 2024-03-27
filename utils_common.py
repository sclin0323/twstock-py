import pandas as pd
import pandas_ta as ta
import numpy as np
import yfinance as yf

from utils_fugle import fugle_get_intraday_meta


def fetch_strategy_raw_data(symbolId, start_date, end_date):

    symbolId_yf = str(symbolId) + '.TW'

    fy_df = yf.download(symbolId_yf, start=start_date, end=end_date)
    fy_df = fy_df.reset_index()

    # 更新公司名稱和產業類別
    stock_meta = fugle_get_intraday_meta(str(symbolId))
    fy_df['股票代碼'] = stock_meta['info']['symbolId']
    fy_df['公司名稱'] = stock_meta['meta']['nameZhTw']
    fy_df['產業類別'] = stock_meta['meta']['industryZhTw']

    # 計算20MA
    fy_df.ta.sma(length=20, append=True)

    # 計算 KD 指標
    kd_df = fy_df.ta.kdj()
    fy_df["K"] = kd_df["K_9_3"]
    fy_df["D"] = kd_df["D_9_3"]
    fy_df["B_K"] = fy_df["K"].shift(1)
    fy_df["B_D"] = fy_df["D"].shift(1)

    # 計算MACD
    fy_df.ta.macd(fast=12, slow=26, signal=9, append=True, SimpleMAOscillator=False, SimpleMASignal=False)
    fy_df.drop(columns=['MACDh_12_26_9'], inplace=True)
    fy_df.rename(columns={'MACD_12_26_9':'macd', 'MACDs_12_26_9': 'dif'}, inplace=True)
    fy_df["macd_d"] = fy_df["macd"].shift(1)

    return fy_df



