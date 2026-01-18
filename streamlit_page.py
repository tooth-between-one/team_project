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

st.set_page_config(layout = "wide")

st.sidebar.title("자동차 데이터 통합 시스템")

menu = st.sidebar.radio(
    "메뉴 선택",
    ("🚗 등록 현황", "🔍 현대자동차 FAQ", "🌳 EV무공해차 통합누리집"),
    label_visibility = "collapsed"
)


if menu == "🚗 등록 현황":
    st.title("서울특별시 자치구별 연료별 차량 등록 현황")
    st.subheader("🚗(부릉)🚗")
    st.caption("이 사이트는 서울특별시의 자치구별 연료별 차량 등록 현황을 통해 친환경 차량 사용을 권유하기 위한 사이트입니다.")
    
    st.header("🚗 등록 현황")
    
    connection = mysql.connector.connect(
        host = "localhost",
        user = "ohgiraffers",
        password = "ohgiraffers",
        database = "cardb",
        charset = "utf8mb4"
    )

    with open("서울_자치구_경계_2017.geojson", encoding="utf-8") as json_file:
        geojson_data = json.load(json_file)

    m = folium.Map(
        location = [37.5642135, 127.0016985],     # 서울특별시의 지도 중심 좌표
        zoom_start = 11                           
    )

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
    ).add_to(m)

    col1, col2 = st.columns(2)
    
    with col1:
        map_data = st_folium(m, width=800, height=600)

    if map_data:
        feature = map_data.get("last_active_drawing")
        if feature and "properties" in feature:
            local_name = feature["properties"].get("SIG_KOR_NM")

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

            result = cursor.fetchall()

            df = pd.DataFrame(result, columns = ["local_name", "fuel_name", "car_num"])

            df["car_num"] = pd.to_numeric(df["car_num"]).fillna(0).astype(int)

            with col2:
                st.header(f"{local_name} 연료별 차량 등록 현황")

                chart_df = df[["fuel_name", "car_num"]].set_index("fuel_name")
                st.bar_chart(chart_df)

##############################################################################################################

            co2_factor = {
                "수소": 0,
                "하이브리드": 70,
                "CNG": 120,
                "엘피지": 125,
                "경유": 130,
                "휘발유": 140
            }
            
            df["co2_factor"] = df["fuel_name"].astype(str).str.strip().map(co2_factor).fillna(0).astype(int)
            df["co2_amount"] = df["car_num"] * df["co2_factor"]
            
            total_co2 = int(df["co2_amount"].sum())
            total_local_cars = int(df["car_num"].sum())
            per_co2 = total_co2 / total_local_cars

            col3, col4 = st.columns(2, gap = "large")

            with col3:
                max_amount = 140 

                st.subheader("연료별 CO2 배출 계수")

                fuel_list = ["CNG", "경유", "수소", "엘피지", "하이브리드", "휘발유"]

                for fuel in fuel_list:
                    co2_amount = co2_factor[fuel]
                    theo = co2_amount / max_amount 

                    st.write(f"{fuel}: {co2_amount} g/km")
                    st.progress(theo)

            with col4:
                st.subheader("CO2 추정 배출량")
                st.metric(label = "총합", value = f"{total_co2:,}")

                st.subheader("차량 1대당 CO2 배출량")
                st.metric(label = "평균", value = f"{per_co2:,.2f}")

            st.divider()

#################################################################################################################3

            cursor.close()
            connection.close()

    else:
        st.info("지도에서 자치구를 클릭하면 상세 등록 현황을 확인할 수 있습니다.")

elif menu == "🔍 현대자동차 FAQ":
    st.title("🔍 현대자동차 FAQ")
    st.markdown("---")

    try:
        with open("hyundai_faq.json", "r", encoding="utf-8") as f:
            faq_data = json.load(f)

        category_list = []

        for item in faq_data :
            name = item["category_name"]
            category_list.append(name)

        same_set = set(category_list)

        categories = sorted(list(same_set))

        selected_category = st.selectbox("카테고리를 선택하세요", ["전체"] + categories)

        st.write("")

        for item in faq_data:
            if selected_category == "전체" or item['category_name'] == selected_category:
                with st.expander(f"[{item['category_name']}] {item['question']}"):
                    st.write(item['answer'])

    except FileNotFoundError:
        st.error("hyundai_faq.json 파일을 찾을 수 없습니다. 파일 경로를 확인해주세요.")
    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")

elif menu == "🌳 EV무공해차 통합누리집" :
    st.title("🌳 EV무공해차 통합누리집 보험금 / FAQ")
    