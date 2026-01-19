"""
folium doc.
https://python-visualization.github.io/folium/latest/user_guide/geojson/geojson.html

자치구 json
https://github.com/lifeisgoodlg/Korea_District/tree/master
"""

import json
import folium
import altair as alt
import mysql.connector
import streamlit as st
import pandas as pd
from streamlit_folium import st_folium

# =========================
# Streamlit 기본 설정
# =========================
st.set_page_config(layout="wide")

st.sidebar.title("ROKa_T")

if "menu" not in st.session_state:
    st.session_state.menu = "🚗 등록 현황"

menu_options = ("🚗 등록 현황", "🔍 현대자동차 FAQ", "🌳 EV무공해차 통합누리집")

menu = st.sidebar.radio(
    "메뉴 선택",
    menu_options,
    index=menu_options.index(st.session_state.menu),
    label_visibility="collapsed"
)

st.session_state.menu = menu


# =========================
# 🚗 등록 현황 페이지
# =========================
if menu == "🚗 등록 현황":
    st.title("ROKa-T", text_alignment="center")
    st.subheader("🚗차량 등록 데이터로 측정하는 도시 환경오염의 지표🚗")
    st.markdown("원하는 지역에 마우스를 대보세요! 🖱️  \n우리 지역의 자동차 등록현황과 연료 사용량을 확인할 수 있어요 🔍 ")

    connection = mysql.connector.connect(
        host="localhost",
        user="ohgiraffers",
        password="ohgiraffers",
        database="cardb",
        charset="utf8mb4"
    )

    with open("../data/seoul_2017.geojson", encoding="utf-8") as f:
        geojson_data = json.load(f)

    m = folium.Map(
        location=[37.5642135, 127.0016985],
        zoom_start=11
    )

    folium.GeoJson(
        geojson_data,
        tooltip=folium.GeoJsonTooltip(
            fields=["SIG_KOR_NM"],
            aliases=["지역구: "]
        ),
        highlight_function=lambda feature: {
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

            st.divider()
            st.header(f"📍 {local_name} 상세 통계")

            cursor = connection.cursor()

            sql = """
                SELECT l.local_name, f.fuel_name, SUM(r.car_num)
                FROM reg_info r
                JOIN local_info l ON r.local_id = l.local_id
                JOIN fuel_info f ON r.fuel_id = f.fuel_id
                JOIN car_info c ON r.car_id = c.car_id
                WHERE l.local_name = %s
                GROUP BY l.local_name, f.fuel_name
            """

            cursor.execute(sql, (local_name,))
            result = cursor.fetchall()

            df = pd.DataFrame(result, columns=["local_name", "fuel_name", "car_num"])
            df["car_num"] = pd.to_numeric(df["car_num"]).fillna(0).astype(int)

            with col2:
                st.subheader(f"{local_name} 연료별 차량 등록 현황")

                chart_df = df[["fuel_name", "car_num"]]

                chart = (
                    alt.Chart(chart_df)
                    .mark_bar()
                    .encode(
                        x=alt.X(
                            "fuel_name:N",
                            title="연료",
                            axis=alt.Axis(labelAngle=0)  # 가로축 글씨 가로
                        ),
                        y=alt.Y(
                            "car_num:Q",
                            title="등록 대수"
                        )
                    )
                )

                st.altair_chart(chart, use_container_width=True)

            co2_factor = {
                "휘발유": 140,
                "경유": 130,
                "엘피지": 125,
                "CNG": 120,
                "하이브리드": 70,
                "수소": 0
            }

            df["co2_factor"] = df["fuel_name"].map(co2_factor).fillna(0)
            df["co2_amount"] = df["car_num"] * df["co2_factor"]

            total_co2 = int(df["co2_amount"].sum())
            total_cars = int(df["car_num"].sum())
            avg_co2 = total_co2 / total_cars if total_cars else 0

            col3, col4 = st.columns(2, gap="large")

            with col3:
                st.subheader("연료별 CO₂(g/kg) 배출 순위")
                for i, (fuel, value) in enumerate(co2_factor.items(), start=1):
                    st.write(f"{i}. {fuel}: {value} g/km")
                    st.progress(value / 140)

                with st.container(border=True):
                    st.subheader("🚗 연 15,000km 주행 기준")
        
                    c1, c2 = st.columns(2)
                    c1.metric("가솔린", "2.1톤")
                    c2.metric("하이브리드", "1.05톤")
                    
                    st.divider()
                    st.markdown("#### ❓ 이 1톤이 어느 정도냐면?")
                    
                    comparison_data = {
                        "환산 기준": ["소나무 흡수량", "성인 1인 연간 호흡 배출", "석탄 발전 전력", "비행기 서울↔부산"],
                        "수치": ["약 150그루 / 1년", "약 2톤", "약 400 kWh", "약 20회"]
                    }
                    st.table(pd.DataFrame(comparison_data))
            with col4:
                st.subheader('⬇️ 이 지역의 배출량💨')
                st.metric("총합(CO₂ 추정 배출량)", f"{total_co2:,}")
                st.subheader('⬇️ 이 지역의 온도🌡️')
                st.metric("차량 1대당 평균", f"{avg_co2:,.2f}")
                st.image('../data/car_car.png')

            if st.button("🌳 EV무공해차 통합누리집으로 이동"):
                st.session_state.menu = "🌳 EV무공해차 통합누리집"
                st.rerun()

            cursor.close()
            connection.close()

    else:
        st.info("지도에서 자치구를 클릭하면 상세 정보를 확인할 수 있습니다.")

# =========================
# 🔍 현대자동차 FAQ
# =========================
elif menu == "🔍 현대자동차 FAQ":
    st.title("🔍 현대자동차 FAQ")
    st.divider()

    try:
        with open("../data/hyundai_faq.json", encoding="utf-8") as f:
            faq_data = json.load(f)

        categories = sorted({item["category_name"] for item in faq_data})
        selected = st.selectbox("카테고리 선택", ["전체"] + categories)

        for item in faq_data:
            if selected == "전체" or item["category_name"] == selected:
                with st.expander(f"[{item['category_name']}] {item['question']}"):
                    st.write(item["answer"])

    except Exception as e:
        st.error(e)

# =========================
# 🌳 EV 무공해차 FAQ
# =========================
elif menu == "🌳 EV무공해차 통합누리집":
    st.title("🌳 EV 무공해차 FAQ")
    st.image("../data/money.png")
    st.divider()

    try:
        with open("../data/ev_faq.json", encoding="utf-8") as f:
            faq_data = json.load(f)

        categories = sorted({item["category_name"] for item in faq_data})
        selected = st.selectbox("카테고리 선택", ["전체"] + categories)

        for item in faq_data:
            if selected == "전체" or item["category_name"] == selected:
                with st.expander(f"[{item['category_name']}] {item['question']}"):
                    st.write(item["answer"])

    except Exception as e:
        st.error(e)