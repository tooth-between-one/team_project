# 정적 크롤링	요청하면 HTML/JSON이 바로 응답
# 동적 크롤링	JS 실행 후에야 데이터 생성

import requests
from bs4 import BeautifulSoup
import json
import html


# FAQ 데이터가 실제로 존재하는 주소
# FAQ 화면 URL 아님
# FAQ 데이터를 json형태로 주는 API 주소
url = "https://www.hyundai.com/kr/ko/gw/customer-support/v1/customer-support/faq/list"

# 이 코드는 FAQ 응답 데이터의 구조를 확인하기 위해 사용
# data 안에 어떤 키가 있는지,
# list 안에 faqQuestion과 faqAnswer가 있는지 확인용 코드
""" load = {
    "searchKeyword": "",
    "pageNo": 1,
    "faqCategoryCode" : "04",
    "pageSize": "10",
    "faqSeq": "",
    "siteTypeCode": "H"
}
response = requests.post(url, json=load)
data = response.json()
print(json.dumps(data))
 """


# payload는 몸통이다.
# 환경이라는 키워드로
# 1페이지를
# 10개씩
# 현대차(H) 사이트 기준으로
# FAQ 목록을 달라 
load = {
    "searchKeyword": "",
    "pageNo": 1,
    "faqCategoryCode" : "04",
    "pageSize": "10",
    "faqSeq": "",
    "siteTypeCode": "H"
}

# 현대차 FAQ 카테고리 코드 목록
# 여러 카테고리의 FAQ를 한 번에 수집하기 위해 리스트로 관리
category_code = ['01', '02', '03', '04', '06', '07', '08', '09', '10']

with open("hyundai_faq.txt", "w", encoding="UTF-8") as f1:
    # 카테고리 코드 하나씩 순회하면서 FAQ 수집
    for code in category_code :
        page = 1

        # 페이지가 더 이상 없을 때까지 반복
        while True :
            # load 안의 값을 code와 page로 갱신한다.
            load["faqCategoryCode"] = code
            load["pageNo"] = page

            # GET -> “이거 줘”
            # 데이터 요청
            # 조건이 URL에 붙음
            # body(몸통) 없음

            # POST -> “이 조건으로 처리해줘”
            # 검색, 필터링, 처리 요청
            # body(payload)에 데이터 포함
            # 구조화된 데이터(JSON) 가능
            response = requests.post(url, json=load)
            data = response.json()

            # searchKeyword="환경" → 검색 조건
            # data → 검색 결과 묶음(몇개의 검색 결과)
            # list → 화면에 보이는 FAQ들
            faqs = data["data"]["list"]
            
            if not faqs :
                break

            for faq in faqs :
                question = faq["faqQuestion"]
                print(faq["faqQuestion"])
                
                un_answer = html.unescape(faq["faqAnswer"])
                answer = BeautifulSoup(un_answer, 'html.parser').get_text('\n').strip()
                print(answer)

                f1.write(f"[카테고리] {faq["faqCategoryName"]}\n")
                f1.write(f"Q. {question}\n")
                f1.write(f"A. {answer}\n")
                f1.write("=" * 80 + "\n")
            
            page = page + 1