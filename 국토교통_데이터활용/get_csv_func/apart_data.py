import requests
import pandas as pd

def apart_get_name():
    df = pd.read_csv("static/csv/apart_data.csv")
    apart_name_to_csv = pd.DataFrame(df['아파트'])
    apart_name_to_csv.to_csv("static/csv/apart_get_name.csv", index=False, header=False)

# apart_get_name()

def apart_get_price():
    df = pd.read_csv("static/csv/apart_data.csv")
    apart_price_to_csv = pd.DataFrame(df['거래금액'])
    apart_price_to_csv['거래금액'] = apart_price_to_csv['거래금액'].str.replace(',', '', regex=False).astype(int).astype(str) #추후 문제 해결 필요
    apart_price_to_csv.to_csv("static/csv/apart_get_price.csv", index=False, header=False)

# apart_get_price()

def apart_get_area():
    df = pd.read_csv("static/csv/apart_data.csv")
    apart_area_to_csv = pd.DataFrame(df['전용면적'])
    apart_area_to_csv.to_csv("static/csv/apart_get_area.csv", index=False, header=False)

# apart_get_area()

"""
최종 아파트 데이터
* 좌표
* 아파트명
* 금액
* 면적적
"""
def total_data():
    t_data = []

    csv_list = ['lat_long', 'apart_get_name', 'apart_get_price', 'apart_get_area']

    for i in csv_list:
        df = pd.read_csv(f"static/csv/{i}.csv")
        t_data.append(df)
    
    merged_df = pd.concat(t_data, axis=1, ignore_index=False) #concat : csv 데이터 합침, axis : 가로 형태로 값을 계속 이어붙힘
    merged_df.to_csv("static/csv/apart_total_data.csv", index=False, header=False)

# total_data()
