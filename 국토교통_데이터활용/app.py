from flask import Flask, request, jsonify
from flask import render_template
import requests
import pandas as pd
import time
import numpy as np
from math import radians

app = Flask(__name__)

# 카카오 REST API 키
REST_API_KEY = "85365dfbcc4b4e710f4b5d5246d462c1"

# Main
# 회사 내 3km 반경 아파트 name, lat, lng 데이터 csv 변경
@app.route("/send_route_data", methods=["POST"])
def receive_apartment_data():
    data = request.get_json()
    apartments = data.get("apartments", [])
    company = data.get("company", [])

    df = pd.DataFrame(apartments)
    df.to_csv("static/location_csv/nearby_apartment_latlng.csv", index=False)

    df2 = pd.DataFrame(company)
    df2.to_csv("static/location_csv/company_latlng.csv", index=False)

    company_to_apartment()

    return jsonify({"message": "success"})

# 회사 -> 거주지 도로 좌표 
def company_to_apartment():
    # kakao mobility API
    url = "https://apis-navi.kakaomobility.com/v1/directions"
    headers = {
        "Authorization": f"KakaoAK {REST_API_KEY}",
        "Content-Type": "application/json"
    }

    # 출발지
    company_latlng = pd.read_csv("static/location_csv/company_latlng.csv")
    company_latlng.columns = ['lat', 'lng']
    lat = company_latlng.iloc[0]['lat']
    lng = company_latlng.iloc[0]['lng']
    company_coords = f"{lng}, {lat}"

    # 목적지(5km 내 아파트)
    destination = pd.read_csv("static/location_csv/nearby_apartment_latlng.csv")

    # 모든 출발지 -> 목적지 리스트
    all_coords = []
    for _, row in destination.iterrows():
        apt_name = row['name']
        destination = f"{row['lng']}, {row['lat']}"
        params = {
            "origin": company_coords,
            "destination": destination,
            "priority": "RECOMMEND",
            "car_fuel": "GASOLINE",
            "car_hipass": False
        }     

        # 요청 보내기
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        print(data)


        if 'routes' in data and data['routes']:
            route = data['routes'][0]

            if route.get('result_code') == 0 and 'sections' in route:
                for section in route['sections']:
                    for road in section.get('roads', []):
                        vertexes = road.get('vertexes', [])
                        coords = list(zip(vertexes[::2], vertexes[1::2]))

                        for lat, lng in coords:
                            all_coords.append({
                                "apartment": apt_name,
                                "lat": lat,
                                "lng": lng
                            })
        time.sleep(0.2)       

        # to_csv
        df = pd.DataFrame(all_coords)
        df.to_csv("static/location_csv/doro_latlng.csv", index=False, header=False)
        
        # 교통량 측정
        traffic_cal()

# 출발지 -> 목적지 교통량 측정
## doro_latlng.csv의 목적지까지 도로 좌표 + linkid_coords_traffic.csv의 교통량 사용
## 도로 좌표에서 10m 이내 좌표 시 트래픽 합산산
def traffic_cal():
    route_df = pd.read_csv("static/location_csv/doro_latlng.csv", header=None)
    route_df.columns = ['apartment', 'lng', 'lat']
        
    traffic_df = pd.read_csv("static/location_csv/linkid_coords_traffic.csv")
    traffic_df = traffic_df[['lat', 'lng', '전일']]

    apartment_info = pd.read_csv("static/location_csv/nearby_apartment_latlng.csv")

    # numpy 배열로 변환 (도로)
    traffic_coords = traffic_df[['lat', 'lng']].to_numpy()
    traffic_volumes = traffic_df['전일'].to_numpy()

    # 거리 계산 함수 (벡터화)
    def haversine_vector(lat1, lng1, lat2_array, lng2_array):
        R = 6371000
        dlat = np.radians(lat2_array - lat1)
        dlon = np.radians(lng2_array - lng1)
        a = np.sin(dlat / 2)**2 + np.cos(radians(lat1)) * np.cos(np.radians(lat2_array)) * np.sin(dlon / 2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        return R * c

    results = []

    # 아파트별 경로를 순회
    for apt_name in route_df['apartment'].unique():
        route_points = route_df[route_df['apartment'] == apt_name][['lat', 'lng']].to_numpy()
        total_traffic = 0

        for lat1, lng1 in route_points:
            distances = haversine_vector(lat1, lng1, traffic_coords[:, 0], traffic_coords[:, 1])
            # 10m 내 좌표
            matched = distances <= 10
            total_traffic += traffic_volumes[matched].sum()

        # 아파트 본 좌표 가져오기
        apt_row = apartment_info[apartment_info['name'] == apt_name]
        if not apt_row.empty:
            apt_lat = apt_row.iloc[0]['lat']
            apt_lng = apt_row.iloc[0]['lng']
            results.append({
                'apartment': apt_name,
                'lat': apt_lat,
                'lng': apt_lng,
                'total_traffic': total_traffic
            })

    result_df = pd.DataFrame(results)
    result_df.to_csv("static/location_csv/traffic_cal.csv")

def map():
    return render_template("index.html")

@app.route("/")
def index():
    budget = request.args.get("budget", default=100000, type=int)
    area = request.args.get("area", default=60, type=float)
    work_address = request.args.get("work_address", default="서울특별시 중구 세종대로 110", type=str)
    use_radius = 'use_radius' in request.args
    return render_template("index.html", budget=budget, area=area, work_address=work_address, use_radius=use_radius)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)