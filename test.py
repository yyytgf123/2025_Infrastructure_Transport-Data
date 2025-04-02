import matplotlib.pyplot as plt
import pandas as pd
#Geo
import geopandas as gpd
import pyproj



# 위경도 좌표계로 변환
def doro_to_latlong():
    gdf = gpd.read_file("doro/gyeongnam_level5_5_link_2022.shp")
    data_store = []
    target_crs = pyproj.CRS.from_epsg(4326)
    gdf_transformed = gdf.to_crs(target_crs)
    data_store.append(gdf_transformed)

    print(data_store)

    df = pd.DataFrame(data_store[0])
    df.to_csv("static/csv/doro_to_latlong.csv", index=False, header=True)
        
# doro_to_latlong()
    

def doro_to_latlong2():
    df = pd.read_csv("static/csv/trafficvolume.csv")
    df.replace(" ",",")
    df2 = pd.DataFrame(df).replace(" ", ",")
    df2.to_csv("static/csv/trafficvolume2.csv", index=False)

doro_to_latlong2()

#진행
#1. trafficvolume.csv 공백 -> , 변경
#2. linkid -> 위경도 변환
#3. 위경도 변환 -> map에 표시