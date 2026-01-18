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
    ("🚗 등록 현황", "🔍 현대자동차 FAQ", "🌳 EV무공해차 통합누리집"),
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
    with open("seoul_2017.geojson", encoding="utf-8") as json_file:
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
elif menu == "🔍 현대자동차 FAQ":
    st.title("🔍 현대자동차 FAQ")
    st.markdown("---")

    try:
        with open("hyundai_faq.json", "r", encoding="utf-8") as f:
            faq_data = json.load(f)

        # 카테고리별로 모아보기 위해 카테고리 리스트 추출 (중복 제거)
        category_list = []

        # category_list는 리스트였지만, 중간에 중복을 제거하려고 set 주머니에 넣었기 때문에, 다시 사용하기 편한 리스트 주머니로 옮겨 담는 과정이라고 이해하시면 됩니다!
        for item in faq_data :
            name = item["category_name"]
            category_list.append(name)
        
        # set()을 하는 순간, '리스트'가 '집합'으로 변합니다.
        # {"차량구매", "차량정비", "기타"}  <-- 대괄호[]가 아니라 중괄호{}가 됩니다!
        same_set = set(category_list)

        # sorted()는 리스트 형태를 입력받는 것을 좋아합니다.
        # 또한, set(집합)은 순서가 없어서 "기타, 차량정비, 차량구매" 순으로 뒤죽박죽일 수 있습니다.
        # 그래서 다시 리스트로 감싸서 순서를 고정해 주는 것입니다.
        categories = sorted(list(same_set))

        # 사이드바나 상단에 필터 추가 (선택 사항)
        selected_category = st.selectbox("카테고리를 선택하세요", ["전체"] + categories)

        st.write("") # 간격 띄우기

        # 필터링 로직 (사용자가 선택한 카테고리만 보여주기)
        # 사용자가 '전체'를 골랐거나, 현재 항목의 카테고리가 사용자가 선택한 것과 일치할 때만 실행합니다.
        for item in faq_data:
            # 선택한 카테고리만 보여주기 (필터링 로직)
            if selected_category == "전체" or item['category_name'] == selected_category:
                # 제목에 카테고리를 작게 표시하고 질문을 넣음
                with st.expander(f"[{item['category_name']}] {item['question']}"):
                    st.write(item['answer'])

    except FileNotFoundError:
        st.error("hyundai_faq.json 파일을 찾을 수 없습니다. 파일 경로를 확인해주세요.")
    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")

elif menu == "🌳 EV무공해차 통합누리집" :
    st.title("🌳 EV무공해차 통합누리집 보험금 / FAQ")
    