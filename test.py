import requests

url = "https://api.odcloud.kr/api/15037585/v1/uddi:a894e23d-13b4-40e9-9de9-b30e04847e96" 

params = {
    "serviceKey": "ae3823b03d788fc0f5107d09b4b50510f15a12e2c342b55c8c3b55962cf2ae73",
    "page": 1,
    "perPage": 20, # 더 많은 연료 종류를 보기 위해 늘림
    "returnType": "JSON"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    content = response.json()
    items = content.get('data', [])
   
    # 결과를 담을 리스트 (나중에 분석하기 편함)
    result_list = []

    for item in items:
        # 데이터가 없을 경우를 대비해 0을 기본값으로 설정
        def to_int(value):
            try:
                return int(value) if value else 0
            except:
                return 0

        fuel = item.get('연료별')
        
        # 각 차종별 합산 (비사업용 + 사업용)
        sedan = to_int(item.get('승용 비사업용')) + to_int(item.get('승용 사업용'))
        bus = to_int(item.get('승합 비사업용')) + to_int(item.get('승합 사업용'))
        special = to_int(item.get('특수 비사업용')) + to_int(item.get('특수 사업용'))
        truck = to_int(item.get('화물 비사업용')) + to_int(item.get('화물 사업용'))
        
        # 출력
        print(f"연료: {fuel:<8} | 승용: {sedan:>6} | 승합: {bus:>5} | 특수: {special:>5} | 화물: {truck:>6}")
else:
    print(f"Error: {response.status_code}")

# 정석원