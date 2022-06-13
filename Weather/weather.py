from urllib import response
import requests

# 取得未來8小時的天氣預報
def getWeather(url):
    data = requests.get(url)   # 取得 JSON 檔案的內容為文字
    data_json = data.json()    # 轉換成 JSON 格式
    location = data_json['cwbopendata']['dataset']['location']

    for i in location:
        city = i['locationName']    # 縣市名稱
        wx8 = i['weatherElement'][0]['time'][0]['parameter']['parameterName']    # 天氣現象
        maxt8 = i['weatherElement'][1]['time'][0]['parameter']['parameterName']  # 最高溫
        mint8 = i['weatherElement'][2]['time'][0]['parameter']['parameterName']  # 最低溫
        ci8 = i['weatherElement'][2]['time'][0]['parameter']['parameterName']    # 舒適度
        pop8 = i['weatherElement'][2]['time'][0]['parameter']['parameterName']   # 降雨機率
        print(f'{city}未來 8 小時{wx8}，最高溫 {maxt8} 度，最低溫 {mint8} 度，降雨機率 {pop8} %')
        
def getPM2dot5(pm_url):
    data = requests.get(pm_url)
    data_json = data.json()
    records = data_json['records']
    for i in records:
        site = i['sitename']
        county = i['county']
        pm25 = i['pm2.5']
        time = i['publishtime']
        print(f'{county} {site}，pm2.5數值{pm25}，資料時間 {time}')
    
if __name__=="__main__":
    url = 'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization=CWB-A89DDEBE-215B-4AE4-AA1B-7A7F52C58235&downloadType=WEB&format=JSON'
    getWeather(url)
    pm_url = 'https://data.epa.gov.tw/api/v2/aqx_p_432?api_key=fdac918f-b34b-4dd6-94b2-338ea65d1a3f&format=json'
    getPM2dot5(pm_url)   