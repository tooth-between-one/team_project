from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pymysql

results = []

# 1. chrome
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 2. url 
url = 'https://ev.or.kr/nportal/buySupprt/initBuySubsidySupprtAction.do'
driver.get(url)
time.sleep(2) 

boxes = driver.find_elements(By.CLASS_NAME, "subConBox")

for i, box in enumerate(boxes, 1):
    try:
        title = box.find_element(By.CSS_SELECTOR, "h4.subConBoxTit").text
    except:
        title = ""

    try:
        subtitle = box.find_element(By.CSS_SELECTOR, "h5.subConBoxSecTit").text
    except:
        subtitle = "" 

    try:
        uls = box.find_elements(By.TAG_NAME, "ul")
        desc = "" 
        for u in uls:
            if u.text.strip() != "":
                desc = desc + u.text + "\n"
    except:
        desc = ""

    if title and title != "":
        results.append({
            'title': title,
            'subtitle': subtitle,
            'description': desc
        })

driver.quit()

# 저장
conn = pymysql.connect(
    host="localhost",
    user="ohgiraffers",     
    password="ohgiraffers",   
    database="qnadb"
)
cursor = conn.cursor()

query = """
    INSERT INTO tbl_qan (title, subtitle, description) VALUES (%s, %s, %s)
"""

for item in results:
    data = (item['title'], item['subtitle'], item['description'])
    cursor.execute(query, data)

conn.commit()
conn.close()
