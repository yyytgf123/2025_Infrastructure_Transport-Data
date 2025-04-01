#국토교통부_개별공시지가속성조회
import requests
import xml.etree.ElementTree as ET

url = "http://api.vworld.kr/ned/data/getIndvdLandPriceAttr"
params = {
    "key": "API기입",
    "pnu": "1111017700102110000",
    "stdrYear": "2015",
    "format": "xml",
    "numOfRows": "10",
    "pageNo": "1"
}

response = requests.get(url, params=params)
root = ET.fromstring(response.text)

print(response.text)
    
for item in root.iter("field"):
    ldcodenm = item.findtext("ldCodeNm").strip() #법정동 명칭
    pblntfpclnd = item.findtext("pblntfPclnd").strip() #개별공시지가
    stdryear = item.findtext("ldCodeNm").strip() #기준 연도
    mnnmslno = item.findtext("mnnmSlno").strip() #지번

    print(ldcodenm)
    print(pblntfpclnd)
    print(stdryear)
    print(mnnmslno)
