from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup


item1 = input()  # 欲搜尋的產品名稱
min_price1 = int(input())  # 產品1的最低價格
max_price1 = int(input())  # 產品1的最高價格

options = Options()
options.add_argument("--disable-notifications")


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://24h.pchome.com.tw/")
search_bar = driver.find_element(By.ID, "keyword")
search_bar.send_keys(item1)
search_bar.send_keys(Keys.RETURN)

minprice_bar = driver.find_element(By.ID, "MinPrice")
minprice_bar.send_keys(min_price1)

maxprice_bar = driver.find_element(By.ID, "MaxPrice")
maxprice_bar.send_keys(max_price1)
maxprice_bar.send_keys(Keys.RETURN)


time.sleep(1000)
