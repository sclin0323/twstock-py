import config_sys
import pandas as pd

from utils_common import fetch_strategy_raw_data

start_date = '2020-01-01'
end_date = '2024-03-23'

res_df = pd.DataFrame()

for tw_stock_id in config_sys.tw_stock_ids:

    raw_df = fetch_strategy_raw_data(tw_stock_id, start_date, end_date)

    ####################### 交易策略01 #######################
    # 計算進場與出場時機
    # 進場: K值小於30時進場 & MACD趨勢向上
    # 出場: K值大於30且出現死亡交叉 & MACD呈現死叉 & 股價低於20日線
    buyF = False
    buyOrsell = []
    for i in range(len(raw_df)):
        if raw_df["K"][i] < 30 and raw_df["macd"][i] > raw_df["macd_d"][i] and buyF == False :
            buyOrsell.append(1)  # KD值小於30時進場
            buyF = True
        elif (raw_df["K"][i] > 30 and raw_df["B_K"][i] > raw_df["B_D"][i]) and (raw_df["macd"][i] < raw_df["dif"][i]) and (raw_df["Close"][i] < raw_df["SMA_20"][i]) and buyF == True:
            buyOrsell.append(-1)  # KD大於30且出現死亡交叉時出場
            buyF = False
        else:
            buyOrsell.append(0)

    raw_df["buyOrsell"] = buyOrsell
    raw_df[raw_df["buyOrsell"].isin([-1]) | raw_df["buyOrsell"].isin([1])]

    res_df = pd.concat([res_df, raw_df])


res_df.to_csv('./output/20240327.csv', index=False)
    