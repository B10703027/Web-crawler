from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# 函數＿分辨有無現貨
def can_buy(product_info):
    situation = product_info.find('p', {'class': 'iconArea'})
    situation = situation.getText()
    if situation == '可訂購時通知我':
        return False
    else:
        return True

# 消費者輸入欲收尋商品之關鍵字、最低價、最高價
keywords = input('搜尋商品：').split(' ')
min_price_list = []
max_price_list = []
for i in range(len(keywords)):
    min_price = int(input('最低價：'))
    min_price_list.append(min_price)
    max_price = int(input('最高價：'))
    max_price_list.append(max_price)
amount_find = int(input('找尋商品筆數：'))

# 打開 google chrome 瀏覽器，進入 momo 購物平台首頁
chromedriver = '/usr/local/chromedriver'
driver = webdriver.Chrome('./chromedriver')
driver.get('https://www.momoshop.com.tw')
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'lbtclass')))

for i in range(len(keywords)):
    # 自動輸入商品關鍵字
    keyword_ = keywords[i]
    search = driver.find_element_by_name('keyword')
    search.clear() # 搜尋欄位清空
    search.send_keys(keyword_)
    search.submit()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'pageArea')))

    # 自動輸入最低價 & 最高價
    min_price_ = min_price_list[i]
    max_price_ = max_price_list[i]
    floor_price = driver.find_element_by_id('priceS')
    floor_price.send_keys(min_price_)
    ceiling_price = driver.find_element_by_id('priceE')
    ceiling_price.send_keys(max_price_)
    button_price = driver.find_element_by_class_name('priceBtn')
    button_price.click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'pageArea')))

    now_amount = 0 # 目前成功搜尋到有現貨的商品有幾項
    page = 0 # 目前所在搜尋頁頁數

    while now_amount < amount_find:
        page += 1
        button_next = driver.find_element_by_link_text(f'{page}')
        button_next.click()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'pageArea')))

        # 取得原始碼，並用 BeautifulSoup 解析
        soup = BeautifulSoup(driver.page_source, "lxml")
        product_infos = soup.find_all('li', {'is18goods': '0'})

        # 找出商品資訊(名稱、價格、運費、網址)
        for product_info in product_infos:
            if now_amount == amount_find:
                break
            elif can_buy(product_info) == True:
                now_amount += 1
                # 商品名稱
                title = product_info.find('h3', {'class': 'prdName'})
                print(title.getText(), end=' ')    

                # 商品價格
                price = product_info.find('span', {'class': 'price'})
                price = price.getText().split('$')
                if ',' in price[1]:
                    price = price[1].split(',')
                    price_str = str()
                    for i in range(len(price)):
                        price_str += price[i]
                    price = int(price_str)
                else:
                    price = int(price[1])
                print(price, end=' ')
                    
                # 商品運費
                delivery_fee = 0 # 一般宅配商品免運費
                icon_faster = product_info.find('i', {'style': 'background-color: #BE0211; color:#FFFFFF'})
                icon_fresh = product_info.find('i', {'style': 'background-color: #2E97C8; color:#FFFFFF'})
                # 快速到貨未滿 490 元，運費 75 元
                if icon_faster:
                    if icon_faster.getText() == '速':
                        if price < 490:
                            delivery_fee = 75
                # 生鮮食品未滿 800 元，運費 120 元
                if icon_fresh:
                    if icon_fresh.getText() == '急鮮':
                        if price < 800:
                            delivery_fee = 120
                print(delivery_fee, end=' ')
                
                # 商品網址
                url = product_info.find('a', href=True)
                print(url['href'])

    time.sleep(10)
    driver.back()
    driver.back()

driver.quit()