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
import pandas as pd
from streamlit_folium import st_folium


# --- 사이드바 설정 ---
st.sidebar.title("자동차 데이터 통합 시스템")

menu = st.sidebar.radio(
    "메뉴 선택",
    ("🚗 등록 현황", "🔍 자동차 보험 FAQ"),
    label_visibility="collapsed"
)

if menu == "🚗 등록 현황":
    st.title("서울특별시 자치구별 연료별 차량 등록 현황")
    st.subheader("🚗(부릉)🚗")
    st.caption("이 사이트는 서울특별시의 자치구별 연료별 차량 등록 현황을 통해 친환경 차량 사용을 권유하기 위한 사이트입니다.")
    
    st.header("🚗 등록 현황")
    
    # DB 연결
    connection = mysql.connector.connect(
        host = "localhost",
        user = "ohgiraffers",
        password = "ohgiraffers",
        database = "cardb",
        charset="utf8mb4"
    )

    # geojson 파일 읽기
    with open("서울_자치구_경계_2017.geojson", encoding="utf-8") as json_file:
        geojson_data = json.load(json_file)

    # folium을 이용하여 지도 생성
    m = folium.Map(
        location = [37.5642135, 127.0016985],     # 서울특별시의 지도 중심 좌표
        zoom_start = 11                           
    )

    # 팝업에 띄울 정보
    # popup = folium.GeoJsonPopup(
    #     fields = ["SIG_KOR_NM"],
    #     aliases = [""]
    # )

    # 자치구를 클릭한 동안 팝업이 뜨도록 설정
    folium.GeoJson(
        geojson_data,
        tooltip = folium.GeoJsonTooltip(
            fields = ["SIG_KOR_NM"],
            aliases=["지역구: "]
            ),
        highlight_function = lambda feature: {
            "fillColor": "red",
            "color": "yellow",
            "weight": 3,
            "fillOpacity": 0.3,
        },
        # popup = popup,
        # popup_keep_highlighted = True,
    ).add_to(m)


    # 지도 정보 
    map_data = st_folium(m, width=800, height=600)

    if map_data:
        feature = map_data.get("last_active_drawing")
        if feature and "properties" in feature:
            local_name = feature["properties"].get("SIG_KOR_NM")
            # st.write(local_name)

            st.markdown("---")
            st.header(f"📍 {local_name} 상세 통계")
            
            cursor = connection.cursor()

            sql = """
                SELECT l.local_name, f.fuel_name, sum(r.car_num)
                FROM reg_info r
                    JOIN local_info l ON r.local_id = l.local_id
                    JOIN fuel_info f ON r.fuel_id = f.fuel_id
                    JOIN car_info c ON r.car_id = c.car_id 
                WHERE l.local_name = %s
                group by l.local_name, f.fuel_name
                """

            cursor.execute(sql, (local_name, ) ) 

            result = cursor.fetchall()      # 튜플 
                                            # 자치구별 336개의 행 존재 (12개월 * 7연료 * 4종류) 
            # if result:
            #     for row in result:
            #         st.write(row)

            # 데이터 프레임 생성
            df = pd.DataFrame(result, columns = ["local_name", "fuel_name", "car_num"])

            # 'car_num'의 타입을 int로 변경 
            df["car_num"] = pd.to_numeric(df["car_num"]).astype(int)

            # 그래프 출력
            st.header(f"{local_name} 연료별 차량 등록 현황")
            # st.subheader(local_name)
            chart_df = df[["fuel_name", "car_num"]].set_index("fuel_name")
            st.bar_chart(chart_df)


            cursor.close()
            connection.close()

    else:
        st.info("지도에서 자치구를 클릭하면 상세 등록 현황을 확인할 수 있습니다.")

# --- 2. 자동차 보험 FAQ 페이지 ---
elif menu == "🔍 자동차 보험 FAQ":
    st.title("🔍 자동차 보험 FAQ")
    st.markdown("---")
    
    with st.expander("Q1. 자동차 보험 가입은 의무인가요?"):
        st.write("A. 네, 대한민국에서는 자동차 손해배상 보장법에 따라 자동차 소유자는 책임보험에 반드시 가입해야 합니다.")
    # (이하 FAQ 내용 동일)