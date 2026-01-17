"""
folium doc.
https://python-visualization.github.io/folium/latest/user_guide/geojson/geojson.html

자치구 json
https://github.com/lifeisgoodlg/Korea_District/tree/master
"""

import json
import folium
import mysql.connector
import streamlit as st
from streamlit_folium import st_folium

st.title("서울특별시 자치구별 연료별 차량 등록 현황")
st.subheader("🚗(부릉)🚗")
st.caption("이 사이트는 서울특별시의 자치구별 연료별 차량 등록 현황을 통해 친환경 차량 사용을 권유하기 위한 사이트입니다.")

# geojson 파일 읽기
with open("서울_자치구_경계_2017.geojson", encoding="utf-8") as json_file:
    geojson_data = json.load(json_file)


connection = mysql.connector.connect(
    host = "localhost",
    user = "ohgiraffers",
    password = "ohgiraffers",
    database = "cardb",
    charset="utf8mb4"
)

# folium을 이용하여 지도 생성
m = folium.Map(
    location=[37.5642135, 127.0016985],     # 서울특별시의 지도 중심 좌표
    zoom_start=11                           
)

# 팝업에 띄울 정보
popup = folium.GeoJsonPopup(
    fields=["SIG_KOR_NM"],
    aliases=[""]
)

# 자치구를 클릭한 동안 팝업이 뜨도록 설정
folium.GeoJson(
    geojson_data,
    highlight_function=lambda feature: {
        "fillColor": "red",
        "color": "red",
        "weight": 3,
        "fillOpacity": 0.3,
    },
    popup=popup,
    popup_keep_highlighted=True,
).add_to(m)


# 지도 정보 
map_data = st_folium(m, width=800, height=600)