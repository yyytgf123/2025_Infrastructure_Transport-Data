import geopandas as gpd

shapefile_path = "국토교통_데이터활용/static/shp/seoul_node_lev6_2022.shp"
gdf = gpd.read_file(shapefile_path, encoding="cp949")

gdf.to_csv("seoul_node_lev6.csv", index=False)