import requests



url = "https://api.odcloud.kr/api/15097996/v1/uddi:c6b4e4e2-7548-4e75-b563-b1c100038fc4?page=1&perPage=100&returnType=JSON&serviceKey=ae3823b03d788fc0f5107d09b4b50510f15a12e2c342b55c8c3b55962cf2ae73" 

params = {
    "serviceKey": "ae3823b03d788fc0f5107d09b4b50510f15a12e2c342b55c8c3b55962cf2ae73",
    "page": 1,
    "perPage": 100,
    "returnType": "JSON"
}

response = requests.get(url, params)

content = response.json()
items = content.get('data', [])

for item in items:

    place = item.get('시군구별')
    fuel = item.get('연료별')
    tmddyd = item.get('승용')
    tmdgkq = item.get('승합')
    xmrtn = item.get('특수')
    ghkanf = item.get('화물')
    result = item.get('계')

    print(f"시군구별: {place} | 연료별: {fuel} | 승용: {tmddyd} | 승합: {tmdgkq} | 특수: {xmrtn} | 화물: {ghkanf} | 합계: {result}")       # 출력


print("*"*50)
print(items[0].keys()) # 딕셔너리 키값 확인

##ㅇㅁㄴㄹㅇㅁ