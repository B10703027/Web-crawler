from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import random
import re
import pandas as pd

options = Options()
options.add_argument("--disable-notifications")

url = "https://www.cmoney.tw/forum/popular/buzz"
driver = webdriver.Chrome("./chromedriver", options=options)
driver.get(url)

SCROLL_PAUSE_TIME = 1
last_height = driver.execute_script("return document.body.scrollHeight")
# 等待網頁加載完成
start_time = time.time()
soup = BeautifulSoup(driver.page_source, "html.parser")
while True:
    buttons = driver.find_elements(
        By.CLASS_NAME, "btn.text-primary.textRule__btn")
    for button in buttons:
        try:
            wait = WebDriverWait(driver, 20)
            wait.until(EC.element_to_be_clickable(button)).click()
        except:
            driver.execute_script("window.scrollTo(0, 0);")
            button.click()

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    break_outer_loop = False
    if new_height == last_height:
        i = 0
        while i < 5:
            driver.execute_script("window.scrollTo(0, 0);")
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script(
                "return document.body.scrollHeight")
            i += 1
        if new_height == last_height:
            break_outer_loop = True
            break
    last_height = new_height
    if break_outer_loop == True:
        break

sp = BeautifulSoup(driver.page_source, "html.parser")
frames = sp.find_all(class_='page__section bg-light')

times = []  # 時間
topics = []  # 標題
tags = []  # 標籤
contents = []  # 內文
likes = []  # 按讚數
donates = []  # 贊助數
comments = []  # 留言數
for frame in frames:
    time_text = frame.find('a', class_="link member__period text-dark-600")
    if time_text == None:
        times.append('NaN')
    else:
        times.append(time_text.text)

    topic_text = frame.find('h3', class_="articleContent__title text-dark-800")
    if topic_text == None:
        topics.append('NaN')
    else:
        topics.append(topic_text.text[11:-9])

    tag_text = frame.find_all('div', class_="articleTags__text text-dark-800")
    if tag_text == None:
        tags.append('NaN')
    else:
        tag_text_list = []
        for i in range(len(tag_text)):
            tag_text_list.append(tag_text[i].text[17:-15])
        tags.append(tag_text_list)

    content_text = frame.find('pre', class_="textRule__text text-dark-800")
    if content_text == None:
        contents.append('NaN')
    else:
        contents.append(content_text.text.replace('\n', ''))

    like_text = frame.find(
        'div', class_="articleResponse__number text-dark-600")
    if like_text == None:
        likes.append('NaN')
    else:
        likes.append(int(like_text.text[9:-7]))

    donate_text = frame.find(
        'div', class_="articleResponse__donate articleResponse__text--donate text-warning")
    if donate_text == None:
        donates.append('NaN')
    else:
        donates.append(int(donate_text.text[9:-8]))

    comment_text = frame.find(
        'button', class_="btn articleResponse__comment text-dark-600")
    if comment_text == None:
        comments.append('NaN')
    else:
        comments.append(int(comment_text.text[7:-8]))

result = {
    "tag": tags,
    "topic": topics,
    "content": contents,
    "like": likes,
    "donate": donates,
    "comment": comments
}

df = pd.DataFrame(result)
# print(df)
df.to_csv("CMoney.csv")

time.sleep(2)

driver.close()
