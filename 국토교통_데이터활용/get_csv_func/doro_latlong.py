import geopandas as gpd

shapefile_path = "static/shp/seoul_level5_5_link_2022.shp" 

gdf = gpd.read_file(shapefile_path)

if gdf.crs != "EPSG:4326":
    gdf = gdf.to_crs(epsg=4326)

gdf["longitude"] = gdf.geometry.centroid.x
gdf["latitude"] = gdf.geometry.centroid.y

columns_to_keep = ["k_link_id","latitude","longitude","road_rank"]

gdf[columns_to_keep].to_csv("static/csv/doro_latlong.csv", index=False)

