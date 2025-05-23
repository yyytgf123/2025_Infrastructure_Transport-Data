import folium

# 시작점과 끝점
point1 = (37.49806381753669, 126.84829667181845)
point2 = (37.4982223874875, 126.85006623998545)

# 지도 생성
m = folium.Map(location=point1, zoom_start=16)
folium.Marker(point1, tooltip='Start').add_to(m)
folium.Marker(point2, tooltip='End').add_to(m)
folium.PolyLine([point1, point2], color='blue').add_to(m)

# 저장
m.save('link_1013669.html')
