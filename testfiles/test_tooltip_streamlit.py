import json
import folium
import mysql.connector
import streamlit as st
import pandas as pd
from streamlit_folium import st_folium

# --- 사이드바 설정 ---
st.sidebar.title("자동차 데이터 통합 시스템")

menu = st.sidebar.radio(
    "메뉴 선택",
    ("🚗 등록 현황", "🔍 자동차 보험 FAQ"),
    label_visibility="collapsed"
)

# --- 1. 등록 현황 페이지 ---
if menu == "🚗 등록 현황":
    st.title("서울특별시 자치구별 연료별 차량 등록 현황")
    st.subheader("🚗(부릉)🚗")
    st.caption("이 사이트는 서울특별시의 자치구별 연료별 차량 등록 현황을 통해 친환경 차량 사용을 권유하기 위한 사이트입니다.")
    
    st.header("🚗 등록 현황")

    # GeoJSON: 지도의 '구 경계선'을 그리기 위한 좌표 데이터입니다.
    with open("seoul_2017.geojson", encoding="utf-8") as json_file:
        geojson_data = json.load(json_file)

    # DB 연결
    connection = mysql.connector.connect(
        host = "localhost",
        user = "ohgiraffers",
        password = "ohgiraffers",
        database = "cardb",
        charset="utf8mb4"
    )
    # 서울 중심 좌표로 지도 초기화
    m = folium.Map(location=[37.5642135, 127.0016985], zoom_start=11)

    # 자치구 경계선 그리기 및 툴팁 설정
    folium.GeoJson(
        geojson_data,
        # lambda: "지금부터 이름 없는 함수를 만들겠다"는 선언입니다.
        # feature: Folium이 넘겨주는 해당 구역의 데이터(GeoJSON의 속성값 등)를 받는 변수입니다.
        highlight_function=lambda feature: { # 마우스 올렸을 때 효과
            "fillColor": "red",
            "color": "yellow",
            "weight": 3,
            "fillOpacity": 0.3,
        },
        # 마우스를 올리면 구 이름이 뜨도록 설정
        tooltip=folium.GeoJsonTooltip(fields=["SIG_KOR_NM"], aliases=["지역구: "])
    ).add_to(m)

    # 지도 출력
    map_data = st_folium(m, width=800, height=600)

    # --- 클릭 시 데이터 표시 로직 (여기가 핵심입니다) ---
    # 지도에서 일어난 클릭, 마우스 이동, 줌(Zoom) 정보가 모두 담긴 커다란 딕셔너리(Dictionary)입니다.
    # ["last_active_drawing"]: 클릭된 도형(자치구 한 칸) 전체 정보를 가져옵니다.
    # ["properties"]: 그 도형이 가진 속성 정보(데이터) 바구니를 엽니다.
    # ["SIG_KOR_NM"]: 그 바구니 안에서 아까 배운 지역구 한국어 명칭이라는 키워드를 찾아 실제 값(예: "강남구")을 꺼냅니다.
    if map_data and map_data.get("last_active_drawing"):
        selected_gu = map_data["last_active_drawing"]["properties"]["SIG_KOR_NM"]
        
        st.markdown("---")
        st.header(f"📍 {selected_gu} 상세 통계")

        # 1월 데이터를 기준으로 가져오는 예시 쿼리
        # fuel_name별 합계 쿼리
        query_fuel = f"SELECT fuel_name, SUM(car_num) as total FROM 테이블명 WHERE local_name = '{selected_gu}' GROUP BY fuel_name"
        # car_type별 합계 쿼리
        query_type = f"SELECT car_type, SUM(car_num) as total FROM 테이블명 WHERE local_name = '{selected_gu}' GROUP BY car_type"
        
        # [연료별 합계 표시]
        st.subheader("⛽ 연료별 등록 현황")
        
        st.info(f"{selected_gu}의 연료별/차종별 데이터가 이 아래에 순차적으로 표시됩니다.")
        
        # [차종별 합계 표시]
        st.subheader("🚙 차종별 등록 현황")
    else:
        st.info("지도에서 자치구를 클릭하면 상세 등록 현황을 확인할 수 있습니다.")

# --- 2. 자동차 보험 FAQ 페이지 ---
elif menu == "🔍 자동차 보험 FAQ":
    st.title("🔍 자동차 보험 FAQ")
    st.markdown("---")
    
    with st.expander("Q1. 자동차 보험 가입은 의무인가요?"):
        st.write("A. 네, 대한민국에서는 자동차 손해배상 보장법에 따라 자동차 소유자는 책임보험에 반드시 가입해야 합니다.")
    # (이하 FAQ 내용 동일)