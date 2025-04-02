import requests
import xml.etree.ElementTree as ET
import pandas as pd

service_key = "1859367345"
url = "https://data.ex.co.kr/openapi/trafficapi/trafficAll"

def traffic_data():
    params = {
        'key' : service_key,
        'type' : 'xml',
        'tmType' : "1"
    }
    response = requests.get(url, params=params)
    root = ET.fromstring(response.text)

    print(response.text)

    sum_data = []
    for item in root.iter("trafficAll"):
        exDivCode = item.findtext("exDivName")
        trafficAmout = item.findtext("trafficAmout")    
        sumTm = item.findtext("sumTm")
        print(f"exDivCdoe : {exDivCode} | trafficAmout : {trafficAmout} | sumTm : {sumTm}")

traffic_data()
