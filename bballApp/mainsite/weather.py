from urllib import response
import requests
import socket
from datetime import datetime

url = 'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization=CWB-A89DDEBE-215B-4AE4-AA1B-7A7F52C58235&downloadType=WEB&format=JSON'
pm_url = 'https://data.epa.gov.tw/api/v2/aqx_p_432?api_key=fdac918f-b34b-4dd6-94b2-338ea65d1a3f&format=json'
target_country = "臺中市"
# import geoip2.database
#
# def location():
#     # This reader object should be reused across lookups as creation of it is
#     # expensive.
#     with geoip2.database.Reader('C:/Users/Rita/Downloads/GeoLite2-City.mmdb') as reader:
#         ip = socket.gethostbyname(socket.gethostname())
#         response = reader.city('203.66.245.21');
#     # reader = geoip2.database.Reader('./GeoLite2-City.mmdb')
#     # ip = raw_input("輸入你要查詢的IP:/n")
#     # response = reader.city(ip)
#     # 有多種語言,我們這裡主要輸出英文和中文
#     print("你查詢的IP的地理位置是:")
#     print("地區:{}({})".format(response.continent.names["es"], response.continent.names["zh-CN"]))
#     print("國家:{}({}) ,簡稱:{}".format(response.country.name, response.country.names["zh-CN"], response.country.iso_code))
#     print("洲/省:{}({})".format(response.subdivisions.most_specific.name,response.subdivisions.most_specific.names))
#     print("城市:{}({})".format(response.city.name, response.city.names))
#     print("經度:{},緯度{}".format(response.location.longitude, response.location.latitude))
#     print("時區:{}".format(response.location.time_zone))
#     print("郵編:{}".format(response.postal.code))


# 取得未來8小時的天氣預報
def getWeather(url):
    data = requests.get(url)  # 取得 JSON 檔案的內容為文字
    data_json = data.json()  # 轉換成 JSON 格式
    location = data_json['cwbopendata']['dataset']['location']

    for i in location:
        city = i['locationName']  # 縣市名稱
        wx8 = i['weatherElement'][0]['time'][0]['parameter']['parameterName']  # 天氣現象
        maxt8 = i['weatherElement'][1]['time'][0]['parameter']['parameterName']  # 最高溫
        mint8 = i['weatherElement'][2]['time'][0]['parameter']['parameterName']  # 最低溫
        ci8 = i['weatherElement'][2]['time'][0]['parameter']['parameterName']  # 舒適度
        pop8 = i['weatherElement'][2]['time'][0]['parameter']['parameterName']  # 降雨機率
        if city == target_country:
            return wx8, maxt8, mint8, ci8, pop8
            # print(f'{city}未來 8 小時{wx8}，最高溫 {maxt8} 度，最低溫 {mint8} 度，降雨機率 {pop8} %，舒適度 {ci8}')


def getPM2dot5(pm_url):
    data = requests.get(pm_url)
    data_json = data.json()
    records = data_json['records']
    site_list = []
    pm25_list = []
    now = datetime.now()
    msg = "現在無法拿到PM2.5的資料"
    if not records:
        return msg, now
    for i in records:
        site = i['sitename']
        county = i['county']
        pm25 = i['pm2.5']
        time = i['publishtime']
    #     if county == target_country:
    #         site_list.append(site)
    #         pm25_list.append(pm25)
    #         print(f'{county} {site}，pm2.5數值{pm25}，資料時間 {time}')
    # return site_list, pm25_list, time
        if county == target_country:
            return pm25, time
    msg = target_country+"現在沒有資料"
    return msg, now


# if __name__ == "__main__":
#     url = 'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization=CWB-A89DDEBE-215B-4AE4-AA1B-7A7F52C58235&downloadType=WEB&format=JSON'
#     getWeather(url)
#     pm_url = 'https://data.epa.gov.tw/api/v2/aqx_p_02?api_key=fdac918f-b34b-4dd6-94b2-338ea65d1a3f&format=json'
#     getPM2dot5(pm_url)
    # location()
