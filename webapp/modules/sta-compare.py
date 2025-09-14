import time
import re
import urllib.parse
from selenium import webdriver
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

def print_atable(atable):
    i = 0
    for arow in atable:
        print(arow)
        i += 1
        if i == 2:
            break

def crawl_9x9(browser, keyword):
    atable = []
    url = 'https://www.9x9.tw/mod/search/result.php?keyword={q}&search_send=1'
    encoded_query = urllib.parse.quote(keyword)
    url = url.format(q=encoded_query)


    print(url)
    browser.get(url)
    time.sleep(0.5)
    bsoup = BeautifulSoup(browser.page_source, 'html.parser')

    product = bsoup.find('div', {'class', 'product'})
    # print(product)
    listarea = product.find('div', {'class', 'listarea'})
    pinfo_list = listarea.find_all('div', {'class', 'pinfo'})

    for pinfo in pinfo_list:
        
        name = pinfo.find('div', {'class', 'name'}).get_text()
        price = pinfo.find('div', {'class', 'price'})
        # print(price)
        op = price.find('div', {'class', 'op'}).get_text()
        bp = price.find('div', {'class', 'bp'})
        if not bp == None:
            bp = bp.get_text()
        lp = price.find('div', {'class', 'lp'})
        if not lp == None:
            lp = lp.get_text()
        tp = price.find('div', {'class', 'tp'})
        if not tp == None:
            tp = tp.get_text()
        looking_more = pinfo.find('div', {'class', 'pic'})
        looking_more = looking_more.find('a')
        if looking_more:
            looking_more = looking_more.get('href')
        else:
            looking_more = None
        
        # print("HELLO", name, market_price, online_price, lp, looking_more)
        atable.append([name, op, bp, lp, tp, looking_more])
        # atable.append(name, market_price, online_price, last_price, looking_more)

    print_atable(atable)
    return atable

def tcsb(browser, q):
    atable = []
    url = 'https://www.tcsb.com.tw/v2/Search?q={q}&order=PriceLowToHigh'


if __name__ == '__main__': # 直接以命令方式執行本程式
    from webutils import *
    from chromed import *
    from ioutils import *
    chrome = webdriver.Chrome(options, service, True)
        
    # search_name = str(input("商品的關鍵字: "))
    # crawl_9x9(chrome, search_name)
    crawl_9x9(chrome, "原子筆")
    chrome.quit()

else: # 以模組方式呼叫本程式的函式
    from webapp.modules.scraper.webutils import *
    from webapp.modules.scraper.chromed import *
    from webapp.modules.scraper.ioutils import *