from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import csv
import json

# 데이터 클래스
class ECOFQAEntry:
    def __init__(self, title, answer):
        self.title = title
        self.answer = answer
    # 딕셔너리 저장
    def to_dict(self):
        return {"title": self.title, "answer": self.answer}

driver = webdriver.Chrome() 
url = "https://ev.or.kr/nportal/partcptn/initFaqAction.do" 
driver.get(url)
time.sleep(2)

result_list = []
page_num = 1

try:
    while True:
        time.sleep(2) 
        faq_titles = driver.find_elements(By.CSS_SELECTOR, 'div.title')
        faq_answers = driver.find_elements(By.CSS_SELECTOR, 'div.faq_con div:not(.answer)')

        for title, answer in zip(faq_titles, faq_answers):
            info = ECOFQAEntry(title.text.strip(), answer.text.strip())
            result_list.append(info)

        #   다음 페이지 버튼 클릭
        try:
            next_arrow = driver.find_element(By.CSS_SELECTOR, "a.next.arrow")
            
            btn_href = next_arrow.get_attribute("href")
            
            if "javascript:goPage" in btn_href:

                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_arrow)
                time.sleep(1)
                
                next_arrow.click()
                page_num += 1

                time.sleep(2) 
            else:
                break
                
        except:
            break

finally:
    driver.quit()

#   파일저장용
now_time = datetime.now().strftime("%y%m%d_%H%M%S")
csv_file_name = f"faq_{now_time}.csv"
json_file_name = f"faq_{now_time}.json"

#   CSV 저장 
with open(csv_file_name, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "answer"])
    writer.writeheader()
    writer.writerows([item.to_dict() for item in result_list])

#   JSON 저장 
with open(json_file_name, "w", encoding="utf-8") as f:
    json.dump([item.to_dict() for item in result_list], f, ensure_ascii=False, indent=4)

# 아직 저장위치 설정전 깃 테스트





