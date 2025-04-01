#국토교통부_건축HUB_건축물대장정보 서비스
import requests
import xml.etree.ElementTree as ET

service_key = "API기입"

url = "http://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo?"

params = {
    'sigunguCd' : '11680',
    'bjdongCd' : '10300',
    'platGbCd' : '0',
    # 'bun' : "0012",
    # 'ji' : '0000',
    'pageNo' : 1,
    'serviceKey' : service_key
}

response = requests.get(url, params=params)
print(response)
root = ET.fromstring(response.text)


for item in root.iter("item"):
    platPlc = item.findtext("platPlc").strip() #대지위치
    crtnDay = item.findtext("crtnDay").strip() #사용 승인일 -> 공급 시점
    etcPurps = item.findtext("etcPurps").strip() #용도정보
    totArea = item.findtext("totArea").strip() #총 면적

    print(platPlc)
    print(crtnDay)
    print(etcPurps)
    print(totArea)