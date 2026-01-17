from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time



path = 'chromedriver.exe'
service = webdriver.chrome.service.Service(path)
driver = webdriver.Chrome(service=service)

# 크롬 열고 2초 쉬기
url = "https://ev.or.kr/nportal/partcptn/initFaqAction.do"
driver.get(url)
time.sleep(2)



FAQ_btn = driver.find_element(By.XPATH, '//*[@id="2"]')
FAQ_btn.click()
time.sleep(1)


items =[]
titles = driver.find_elements(By.CSS_SELECTOR,'div.title')
# for title in titles:
#     print(title.text)

answers = driver.find_elements(By.CSS_SELECTOR, 'div.faq_con div:not(.answer)')
# for answer in answers:
#     print(answer.text)

for title,answer in zip(titles, answers):
    items.append({
            'title' : title.text,
            'answer' : answer.text
    })
    print(title.text)
    print(answer.text)
    print("-"*40)

time.sleep(3)

driver.quit()


