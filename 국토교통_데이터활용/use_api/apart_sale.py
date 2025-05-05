import requests
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import date

service_key = "API기입"
url = "https://apis.data.go.kr/1613000/RTMSDataSvcAptTrade/getRTMSDataSvcAptTrade"
apart_data = []

seoul_lawd_codes = {
    "종로구": "11110", "중구": "11140", "용산구": "11170", "성동구": "11200", "광진구": "11215",
    "동대문구": "11230", "중랑구": "11260", "성북구": "11290", "강북구": "11305", "도봉구": "11320",
    "노원구": "11350", "은평구": "11380", "서대문구": "11410", "마포구": "11440", "양천구": "11470",
    "강서구": "11500", "구로구": "11530", "금천구": "11545", "영등포구": "11560", "동작구": "11590",
    "관악구": "11620", "서초구": "11650", "강남구": "11680", "송파구": "11710", "강동구": "11740"
}

for year in range(2024, 2026):
    for LAWD in seoul_lawd_codes.values():
        for month in range(1, 13):
            ymd = f"{year}{month:02d}"
            params = {
                'serviceKey': service_key,
                'LAWD_CD': LAWD,       # 서울 종로구
                'DEAL_YMD': ymd,     
                'numOfRows': '100',
                'pageNo': '1'
            }

            response = requests.get(url, params=params)
            root = ET.fromstring(response.text)

            for item in root.iter("item"):
                data = {
                    "아파트" : item.findtext("aptNm").strip(), 
                    "동명" : item.findtext("aptDong").strip(), 
                    "법정동" : item.findtext("umdNm").strip(), 
                    "지번" : item.findtext("jibun").strip(),
                    "거래금액" : item.findtext("dealAmount").strip(),
                    "전용면적" : item.findtext("excluUseAr").strip(), 
                    # "거래년도" : item.findtext("dealYear").strip(),
                    # "거래월" : item.findtext("dealMonth").strip(),
                    # "거래일" : item.findtext("dealDay").strip(),
                }
                apart_data.append(data)
        
df = pd.DataFrame(apart_data)
df = df.drop_duplicates(subset=['아파트'], keep="last")
df.to_csv("csv/apart_data.csv", index=False)