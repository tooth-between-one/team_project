# 정적 크롤링	요청하면 HTML/JSON이 바로 응답
# 동적 크롤링	JS 실행 후에야 데이터 생성

import requests
from bs4 import BeautifulSoup
import json
import html

url = "https://www.hyundai.com/kr/ko/gw/customer-support/v1/customer-support/faq/list"

load = {
    "searchKeyword": "",
    "pageNo": 1,
    "faqCategoryCode" : "04",
    "pageSize": "10",
    "faqSeq": "",
    "siteTypeCode": "H"
}

category_code = ['01', '02', '03', '04', '06', '07', '08', '09', '10']

with open("hyundai_faq.txt", "w", encoding="UTF-8") as f1:
    for code in category_code :
        page = 1

        while True :
            load["faqCategoryCode"] = code
            load["pageNo"] = page

            response = requests.post(url, json=load)
            data = response.json()

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