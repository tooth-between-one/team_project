from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import mysql.connector


# 1. chrome 브라우저 실행
path = "chromedriver.exe"
service = webdriver.chrome.service.Service(path)
driver = webdriver.Chrome(service=service)

url = "https://ev.or.kr/nportal/partcptn/initFaqAction.do"
driver.get(url)
time.sleep(1)

# 클릭 버튼 눌러서
news_btn = driver.find_element(By.XPATH, '//*[@id="1"]')
news_btn.click()

time.sleep(5)

# 데이터 가져오기
questions = driver.find_elements(By.CSS_SELECTOR, "div.title")
answers = driver.find_elements(By.CSS_SELECTOR, "div.faq_con div:not(.answer)")

li = []

for question, answer in zip(questions, answers) :
    print("Q")
    li.append({"question" : question.text.strip(), "answer" : answer.text.strip()})
    print("A")
    print("-"*40)

print(li)
print(type(li))

driver.quit()

# db에 저장

connection = mysql.connector.connect(
    host = "localhost",
    user = "ohgiraffers",
    password = "ohgiraffers",
    database = "faqdb"
)

cursor = connection.cursor()

sql = "INSERT INTO faq(question, answer) VALUES (%s, %s)"

for faqs in li :
    cursor.execute(sql,(faqs["question"], faqs["answer"]))      # dict key로 접근하기 위해서는 문자열로 접근 

connection.commit()

cursor.close()
connection.close()