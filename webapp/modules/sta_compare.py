import time
import re
import urllib.parse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from collections import defaultdict

# 自定義模組
from webutils import *
from chromed import *
from ioutils import *

def print_atable(atable):
    print("          商品名稱          |   價格   ")
    for arow in atable:
        alist = []
        for i in range(1, 4):
            if arow[i] is not None:
                alist.append(arow[i])
        if alist:
            print("{:<30} | {:<4}".format(arow[0], min(alist)))


def get_data(keyword):
    service = Service(r"C:\MyProject\webapp\driver\chromedriver-win64.exe")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # 背景執行

    browser = webdriver.Chrome(service=service, options=options)
    try:
        items_9x9 = crawl_9x9(browser, keyword)
        # items_rekuten = crawl_rakuten(browser, table)
        # items_101 = crawl_101(browser, keyword)
        # items_jut = crawl_jet(browser, keyword)
        # 合併結果
        all_items = items_9x9 # + items_rekuten
        return all_items
    finally:
        browser.quit()

# 以 9*9 為主要的搜尋法
def crawl_9x9(browser, keyword):
    url = f"https://www.9x9.tw/mod/search/result.php?keyword={urllib.parse.quote(keyword)}&search_send=1"
    browser.get(url)
    time.sleep(0.2)
    bsoup = BeautifulSoup(browser.page_source, 'html.parser')
    
    datadict = []
    product = bsoup.find('div', {'class': 'product'})
    if not product:
        return datadict

    listarea = product.find('div', {'class': 'listarea'})
    pinfo = listarea.find_all('div', {'class': 'pinfo'})

    for i in range(10): # 只抓取 10 筆資料
        name = pinfo[i].find('div', {'class': 'name'}).get_text()
        price_tags = pinfo[i].find('div', {'class': 'price'})
        prices = []
        for tag in ['op', 'bp', 'lp', 'tp']:
            t = price_tags.find('div', {'class': tag})
            if t:
                price_text = t.get_text()
                price_digits = re.sub(r'[^\d]', '', price_text)
                if price_digits:
                    prices.append(int(price_digits))
        price = min(prices)
        
        link_tag = pinfo[i].find('div', {'class': 'pic'})
        url = link_tag.find('a')['href']
        
        datadict.append({"site": "9x9", "name": name, "price": price, "url": url})
    # search_table = search_imfomation(browser, datadict)

    return datadict # , search_table

def search_imfomation(browser, datadict):
    search_table = []
    for data in datadict:
        url = data['url']
        browser.get(url)
        time.sleep(0.2)
        bsoup = BeautifulSoup(browser.page_source, 'html.parser')
        ul = bsoup.find('ul', {'class': 'info'})
        barcode = ul.find('span', {'id': 'BarCode'}).get_text() # 給 101 以及 金玉堂
        modelcode = ul.find('span', {'id': 'ModelCode'}).get_text() # 給樂天商城
        keyword = data['name'] + " " + modelcode
        search_table.append([barcode, keyword])
    return search_table

def crawl_rakuten(browser, datatable):
    datadict =[]
    for data in datatable:
        url = f"https://www.rakuten.com.tw/search/{urllib.parse.quote(data[1])}/15619/?s=2"
        browser.get(url)
        time.sleep(0.2)
        bsoup = BeautifulSoup(browser.page_source, 'html.parser')
        pinfo = bsoup.find('div', {'class': '_16u6wpdb _6xzpdb8 _6xzpdbg _6xzpdb9j _6xzpdbyh'})
        if pinfo == None:
            datadict.append({'site': 'rakuten', 'name': data["name"], 'price': None, "url": None })
        else:
            price = pinfo.find('div', {'class': "_1md3074m _6xzpdbhq _6xzpdbi5 _6xzpdbyh _6xzpdbew _1md30741b  _6xzpdbh6 _6xzpdbhe _6xzpdbk4 qa-search-price-value"})
            url = pinfo.find('a')['href']

            datadict.append({'site': "rakuten", "name": data['name'], "price": price, "url": url})

    return datadict

def crawl_101():
    pass

# main
if __name__ == '__main__':
    service = Service(r"C:\MyProject\webapp\driver\chromedriver-win64.exe")
    chrome = webdriver.Chrome(service=service, options=options)

   # chrome = webdriver.Chrome(options, service, True)

    try:
        # keyword = str(input("需要搜尋的商品"))
        keyword = "原子筆"
        atable = crawl_9x9(chrome, keyword)

    finally:
        chrome.quit()
