import geopandas as gpd
import pandas as pd

# 1. shapefile 로드
gdf = gpd.read_file("국토교통_데이터활용/static/shp/seoul_level5_5_link_2022.shp")
gdf = gdf.to_crs(epsg=4326)

# 2. 트래픽 CSV 로드
traffic_df = pd.read_csv("국토교통_데이터활용/static/csv/TrafficVolume_LINK_filtered.csv")
link_ids = traffic_df['LINK_ID'].astype(float).astype(int).unique()

# 3. shapefile에서 해당 link_id만 필터링
subset = gdf[gdf['k_link_id'].isin(link_ids)]

# 4. 좌표 펼치기
output = []

for _, row in subset.iterrows():
    link_id = int(row['k_link_id'])
    for lng, lat in row.geometry.coords:
        output.append({
            'LINK_ID': link_id,
            'lat': lat,
            'lng': lng
        })

# 5. DataFrame으로 저장
result_df = pd.DataFrame(output)
result_df.to_csv("국토교통_데이터활용/static/location_csv/link_id_to_latlng.csv", index=False)
