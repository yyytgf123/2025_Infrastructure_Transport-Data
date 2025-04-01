import json
import requests

def get_xy(address):
    try:
        url = "https://dapi.kakao.com/v2/local/search/address.json?query=" + address
        headers = {"Authorization": "KakaoAK API"}

        response = requests.get(url, headers=headers)
        
        json_result = response.json()
        json.dumps(json_result, indent= 4, ensure_ascii=False)

        address_xy = json_result['documents'][0]['address']

        return address_xy['x'], address_xy['y']
    except:
        crd = {"lat":0,"lng":0}
        return crd