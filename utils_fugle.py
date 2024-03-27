import requests
import json

def fugle_get_intraday_meta(symbolId):

    api_token = 'ad1956724a039f66c73e734a61d2fbd3'
    host = 'https://api.fugle.tw'
    endpoint = '/realtime/v0.3/intraday/meta?symbolId='+symbolId+'&apiToken='+api_token;
    url = host + endpoint

    response = requests.get(url)

    if response.status_code == 200:
        response_data = json.loads(response.text)
        return response_data['data']
    else:
        print('請求失敗，狀態碼:', response.status_code)
        return response.text