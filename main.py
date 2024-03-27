import pandas as pd
import pandas_ta as ta
import numpy as np
import yfinance as yf

from datetime import datetime, timedelta

from utils_fugle import fugle_get_intraday_meta

result_df = yf.download('2330.TW', start='2020-01-01', end='2024-03-20')
result_df = result_df.reset_index()

# 更新公司名稱和產業類別
stock_meta = fugle_get_intraday_meta('2330')
result_df['股票代碼'] = stock_meta['info']['symbolId']
result_df['公司名稱'] = stock_meta['meta']['nameZhTw']
result_df['產業類別'] = stock_meta['meta']['industryZhTw']

# 計算20MA
result_df.ta.sma(length=20, append=True)

# 計算 KD 指標
kd_df = result_df.ta.kdj()
result_df["K"] = kd_df["K_9_3"]
result_df["D"] = kd_df["D_9_3"]
result_df["B_K"] = result_df["K"].shift(1)
result_df["B_D"] = result_df["D"].shift(1)

# 計算MACD
result_df.ta.macd(fast=12, slow=26, signal=9, append=True, SimpleMAOscillator=False, SimpleMASignal=False)
result_df.drop(columns=['MACDh_12_26_9'], inplace=True)
result_df.rename(columns={'MACD_12_26_9':'macd', 'MACDs_12_26_9': 'dif'}, inplace=True)
result_df["macd_d"] = result_df["macd"].shift(1)

print(result_df)

#######################################################################################

df_ans = pd.DataFrame([], columns=["Stock", "獲利次數", "虧損次數", "交易次數", "勝率", "最高報酬", "最低報酬", "總報酬", "平均報酬"])

# 計算進場與出場時機
# 進場: K值小於30時進場 & MACD趨勢向上
# 出場: K值大於30且出現死亡交叉 & MACD呈現死叉 & 股價低於20日線
buyF = False
buyOrsell = []
for i in range(len(result_df)):
    if result_df["K"][i] < 30 and result_df["macd"][i] > result_df["macd_d"][i] and buyF == False :
        buyOrsell.append(1)  # KD值小於30時進場
        buyF = True
    elif (result_df["K"][i] > 30 and result_df["B_K"][i] > result_df["B_D"][i]) and (result_df["macd"][i] < result_df["dif"][i]) and (result_df["Close"][i] < result_df["SMA_20"][i]) and buyF == True:
        buyOrsell.append(-1)  # KD大於30且出現死亡交叉時出場
        buyF = False
    else:
        buyOrsell.append(0)

result_df["buyOrsell"] = buyOrsell
result_df[result_df["buyOrsell"].isin([-1]) | result_df["buyOrsell"].isin([1])]

print(result_df)

# 計算買進次數
#buy1 = result_df.loc[result_df["buyOrsell"].isin([1])]
#sell1 = result_df.loc[result_df["buyOrsell"].isin([-1])]
#print("買進次數 : " + str(len(buy1)) + "次")
#print("賣出次數 : " + str(len(sell1)) + "次")


