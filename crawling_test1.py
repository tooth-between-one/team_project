from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager
import time
from urllib.request import urlretrieve
from datetime import datetime


class ECOFQAEntry:
    def __init__(self, title, answer):
        self.title = title
        self.answer = answer

    def __repr__(self):
        return f'{self.title}의 답변 \n{self.answer}'

# Chrome 브라우저 실행
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
tnum = 1 # 뽑아온 데이터의 번호 순서 매김
result_list = []    # 데이터 저장을 위한 리스트 초기화



# url 페이지 접속 
url = "https://ev.or.kr/nportal/partcptn/initFaqAction.do" 
driver.get(url)
time.sleep(1) # 페이지 로딩 대기

# 카테고리 선택 
click3 = driver.find_element(By.ID, '3')
click3.click()
time.sleep(1)

faq_titles = driver.find_elements(By.CSS_SELECTOR, 'div.title')
faq_answers = driver.find_elements(By.CSS_SELECTOR, 'div.faq_con div:not(.answer)')
item_info = zip(faq_titles,faq_answers)

for title,answer in zip(faq_titles,faq_answers):
    eco_fqa_entry = ECOFQAEntry(title.text, answer.text)
    result_list.append(eco_fqa_entry)
    # 터미널에 출력하는용
    # print('*'*50)
    # print(f"{tnum}번 \n제목: {title.text}, \n답변: {answer.text}")
  
for result in result_list:
    print(result)

# 다음페이지로 이동
click_next_page = driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div/div/div[2]/a[4]')
click_next_page.click()
time.sleep(1)

# 페이지 이동후 다시 긁어오기
faq_titles = driver.find_elements(By.CSS_SELECTOR, 'div.title')
faq_answers = driver.find_elements(By.CSS_SELECTOR, 'div.faq_con div:not(.answer)')


for title,answer in zip(faq_titles,faq_answers):

    print('-'*50)
    print(f"{tnum}번 \n제목: {title.text}, \n답변: {answer.text}")
    


#aq_items = driver.find_elements(By.CSS_SELECTOR, 'div.title')

#print(faq_items)
driver.quit()






