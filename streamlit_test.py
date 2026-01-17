import streamlit as st
import pandas as pd


# 1. 페이지 맨위

st.title("ROKa-T : 남한(서울시) 자동차 연료 온도계 ")

st.divider()

st.header("🌡️ 서울시 자치구별 연료 온도계")
st.subheader(" 🚘 우리지역의 자동차 등록 현황은 ?? ")
st.write("지역별 자동차 등록 대수를 온도(°C)로 표현했습니다.")

st.divider() 


# 2. 데이터 ...
data = {
    '지역': ['강남구', '송파구', '서초구', '노원구', '강서구', '마포구', '종로구'],
    '차량수': [50000, 48000, 45000, 35000, 32000, 25000, 15000]
}
df = pd.DataFrame(data)


# 3. 메인으로 ..

# 선택하기 
st.header("1. 우리 동네가 얼마나 뜨거운지 확인해봐요 !! ")
selected_gu = st.selectbox("자치구를 선택하세요", df['지역'])

# 데이터 계산 - 잼민이햄 도움
my_data = df[df['지역'] == selected_gu]
my_count = my_data['차량수'].values[0]
max_count = df['차량수'].max()
temperature = (my_count / max_count) * 100

# 결과 출력
st.metric(label=f"{selected_gu} 등록 대수", value=f"{my_count:,} 대")
st.write(f"🔥 현재 온도는 {int(temperature)}°C 입니다. ")
st.progress(temperature / 100)

# 메시지
if temperature >= 80:
    st.error("🚨 [위험] 매우 뜨겁습니다! 지구가 울어요 😭")
elif temperature >= 50:
    st.warning("⚠️ [주의] 살짝 위험하다 .. !! 😳  ")
else:
    st.success("✅ [양호] 지구가 웃어요 😊 ")

st.divider() 

# 그래프
st.header("2. 서울시 전체 순위")
st.bar_chart(df.set_index('지역'))

st.divider() 

# FAQ
st.header("3. 지구를 식히는 해결책 (FAQ)")

# 버튼 
if st.button("FAQ 보기"):
    
    # 예시 .. (불러오기 ?)
    faq_data = [
        {"Q": "질문", "A": "답"},
        {"Q": "질문", "A": "답"},
        {"Q": "질문", "A": "답"},
        {"Q": "질문", "A": "답"},\
    ]
    

    st.success("정보 로딩 완료 !")
    
    for item in faq_data:
        with st.expander(f"Q. {item['Q']}"):
            st.write(f"A. {item['A']}")