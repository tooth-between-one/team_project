from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import json

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

url = "https://ev.or.kr/nportal/partcptn/initFaqAction.do"
driver.get(url)
time.sleep(2)

results = []
seen = set()  # (category, question) 중복 방지용

try:
    while True:
        time.sleep(1)

        # ✅ FAQ 한 덩어리(카드) 단위로 가져오기
        faq_blocks = driver.find_elements(By.CSS_SELECTOR, "div.board_faq")

        for block in faq_blocks:
            # category_name: span.faq_badge (색상 클래스가 달라도 faq_badge는 공통)
            try:
                category = block.find_element(By.CSS_SELECTOR, "span.faq_badge").text.strip()
            except:
                category = "기타"

            # question: div.title
            try:
                question = block.find_element(By.CSS_SELECTOR, "div.title").text.strip()
            except:
                question = ""

            if not question:
                continue

            # ✅ 답변이 접혀있을 수 있어서 "질문 영역"을 클릭해서 펼친 다음 읽기
            try:
                title_area = block.find_element(By.CSS_SELECTOR, "div.faq_title")
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", title_area)
                time.sleep(0.2)
                title_area.click()
                time.sleep(0.2)
            except:
                pass

            # answer: div.faq_con
            try:
                answer = block.find_element(By.CSS_SELECTOR, "div.faq_con").text.strip()
            except:
                answer = ""

            # 중복 방지
            key = (category, question)
            if key in seen:
                continue
            seen.add(key)

            results.append({
                "category_name": category,
                "question": question,
                "answer": answer
            })

        # ✅ 다음 페이지 클릭 (없거나 더 이상 못 가면 종료)
        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, "a.next.arrow")
            btn_href = next_btn.get_attribute("href") or ""
            btn_class = next_btn.get_attribute("class") or ""

            # 비활성화면 종료 (사이트에 따라 disable/disabled가 붙는 경우가 많음)
            if "disable" in btn_class or "disabled" in btn_class:
                break

            # href가 javascript:goPage(...) 형태면 다음으로 넘어갈 수 있음
            if "javascript:goPage" in btn_href:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)
                time.sleep(0.5)
                next_btn.click()
                time.sleep(2)
            else:
                break

        except:
            break

finally:
    driver.quit()

# ✅ 파일 이름 고정 저장(매번 덮어쓰기)
csv_file_name = "ev_faq.csv"
json_file_name = "ev_faq.json"

with open(csv_file_name, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["category_name", "question", "answer"])
    writer.writeheader()
    writer.writerows(results)

with open(json_file_name, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

print(f"저장 완료: {len(results)}개")
print("CSV:", csv_file_name)
print("JSON:", json_file_name)
