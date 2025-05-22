from flask import Flask, request, jsonify
from flask import render_template
import requests
import pandas as pd

app = Flask(__name__)

# 카카오 REST API 키
REST_API_KEY = "85365dfbcc4b4e710f4b5d5246d462c1"

work_location = {}

@app.route("/set_destination", methods=["POST"])
def set_destination():
    data = request.get_json()
    lat = data.get("aptLat")
    lng = data.get("aptLng")

    if lat is not None and lng is not None:
        destination_location['latlng'].append({"lat": lat, "lng": lng})

        origin = f"{lng}, {lat}"

        set_destination_to_csv(origin)

        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Error"})

def set_destination_to_csv(origin):
    lng, lat = origin.split(", ")
    df = pd.DataFrame(destination_location["latlng"])
    df.to_csv("static/csv2/set_destination_latlng.csv", index=False)

@app.route("/set_work_location", methods=["POST"])
def set_work_location():
    data = request.get_json()
    lat = data.get("lat")
    lng = data.get("lng")

    if lat is not None and lng is not None:
        work_location['lat'] = lat
        work_location['lng'] = lng
        print("받은 직장 좌표:", lat, lng)
        # 서울시청(Test)
        origin = f"{lng},{lat}"

        set_work_location_to_csv(origin)

        return jsonify({"status": "success", "origin": origin})
    return jsonify({"status": "error", "message": "error"})

def set_work_location_to_csv(latlng):
    # kakao mobility API
    url = "https://apis-navi.kakaomobility.com/v1/directions"
    headers = {
        "Authorization": f"KakaoAK {REST_API_KEY}",
        "Content-Type": "application/json"
    }
        
    # 목적지(10km 내 아파트)
    destination = pd.read_csv("static/csv2/set_destination_latlng.csv")

    for _, row in destination.iterrows():
        destination = f"{row['lng']}, {row['lat']}"
        params = {
            "origin": latlng,
            "destination": destination,
            "priority": "RECOMMEND",
            "car_fuel": "GASOLINE",
            "car_hipass": False
        }   

    # 요청 보내기
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    # 도로 경로상의 vertex 좌표 추출
    all_coords = []

    for section in data['routes'][0]['sections']:
        for road in section['roads']:
            vertexes = road['vertexes']
            # (lon, lat) 묶음으로 변환
            coords = list(zip(vertexes[1::2], vertexes[::2]))
            all_coords.extend(coords)

    # 결과 출력
    print("총 좌표 수:", len(all_coords))
    for i, (lng, lat) in enumerate(all_coords[:]): 
        print(f"{i+1}: {lng}, {lat}")

    df = pd.DataFrame(all_coords)
    df.to_csv("static/csv2/set_work_location_latlng.csv", index=False)

destination_location = { "latlng" : []}

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