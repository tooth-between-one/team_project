# 원본 csv 파일에서 그룹화 후 null을 0으로 대체하는 전처리 코드

import pandas as pd

# csv 파일 불러오기
df =  pd.read_csv('서울특별시_자치구별 연료별 자동차 등록현황.csv', encoding='CP949')

# 연료명 바꾸기
df['연료별'] = df['연료별'].str.replace(r'^하이브리드.*','하이브리드', regex=True)
df['연료별'] = df['연료별'].str.replace(r'^휘발유.*','휘발유', regex=True)

# NULL값 0으로 대체
df[['승용', '승합', '화물', '특수']] = (df[['승용', '승합', '화물', '특수']].fillna(0))

# 그룹화
grouped = (
    df.groupby(['년월', '시군구별', '연료별'], as_index=False).agg({
        '승용': 'sum',
        '승합': 'sum',
        '화물': 'sum',
        '특수': 'sum',
        '계': 'sum'
    })
)


# wide → long 변환
df_long = grouped.melt(
    id_vars=['년월', '시군구별', '연료별'],
    value_vars=['승용', '승합', '화물', '특수'],
    var_name='car_type',
    value_name='car_num'
)

# 컬럼명 변경
df_long = df_long.rename(columns={
    '년월': 'reg_date',
    '시군구별': 'local_name',
    '연료별': 'fuel_name'
})

df_long = df_long[
    ['reg_date', 'local_name', 'fuel_name', 'car_type', 'car_num']
]

df_long.to_csv(
    'data2.csv',
    index=False,
    encoding='utf-8-sig'
)

print("CSV 파일 생성 완료")