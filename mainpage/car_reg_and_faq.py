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
# menu = st.sidebar.radio(
#     "메뉴 선택",
#     ("🚗 등록 현황", "🔍 현대자동차 FAQ", "🌳 EV무공해차 통합누리집"),
#     label_visibility="collapsed"
# )

if "menu" not in st.session_state:
    st.session_state.menu = "🚗 등록 현황"

menu_options = ("🚗 등록 현황", "🔍 현대자동차 FAQ", "🌳 EV무공해차 통합누리집")

menu = st.sidebar.radio(
    "메뉴 선택",
    menu_options,
    index=menu_options.index(st.session_state.menu),
    label_visibility="collapsed"
)

# radio에서 바뀐 값 다시 session_state에 반영
st.session_state.menu = menu


# =========================
# 🚗 등록 현황 페이지
# =========================
if menu == "🚗 등록 현황":
    st.title("ROKa-T", text_alignment="center")
    st.subheader("🚗차량 등록 데이터로 측정하는 도시 환경오염의 지표🚗")
    st.caption("자치구별 차량 등록 현황을 통해 친환경 차량 사용을 유도합니다.")

    # DB 연결
    connection = mysql.connector.connect(
        host="localhost",
        user="ohgiraffers",
        password="ohgiraffers",
        database="cardb",
        charset="utf8mb4"
    )

    # GeoJSON 로드
    with open("seoul_2017.geojson", encoding="utf-8") as f:
        geojson_data = json.load(f)

    # 지도 생성
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

            # ---------- 그래프 ----------
            # with col2:
            #     st.subheader(f"{local_name} 연료별 차량 등록 현황")
            #     chart_df = df[["fuel_name", "car_num"]].set_index("fuel_name")
            #     st.bar_chart(chart_df)

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

            # ---------- CO2 분석 ----------
            co2_factor = {
                "수소": 0,
                "하이브리드": 70,
                "CNG": 120,
                "엘피지": 125,
                "경유": 130,
                "휘발유": 140
            }

            df["co2_factor"] = df["fuel_name"].map(co2_factor).fillna(0)
            df["co2_amount"] = df["car_num"] * df["co2_factor"]

            total_co2 = int(df["co2_amount"].sum())
            total_cars = int(df["car_num"].sum())
            avg_co2 = total_co2 / total_cars if total_cars else 0

            col3, col4 = st.columns(2, gap="large")

            with col3:
                st.subheader("연료별 CO₂ 배출 계수")
                for fuel, value in co2_factor.items():
                    st.write(f"{fuel}: {value} g/km")
                    st.progress(value / 140)

            with col4:
                st.subheader("CO₂ 추정 배출량")
                st.metric("총합", f"{total_co2:,}")
                st.metric("차량 1대당 평균", f"{avg_co2:,.2f}")

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
        with open("hyundai_faq.json", encoding="utf-8") as f:
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
    st.divider()

    try:
        with open("ev_faq.json", encoding="utf-8") as f:
            faq_data = json.load(f)

        categories = sorted({item["category_name"] for item in faq_data})
        selected = st.selectbox("카테고리 선택", ["전체"] + categories)

        for item in faq_data:
            if selected == "전체" or item["category_name"] == selected:
                with st.expander(f"[{item['category_name']}] {item['question']}"):
                    st.write(item["answer"])

    except Exception as e:
        st.error(e)