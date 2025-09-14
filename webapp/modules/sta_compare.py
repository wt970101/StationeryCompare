import time
import urllib.parse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def crawl_9x9(browser, keyword):
    atable = []
    url = 'https://www.9x9.tw/mod/search/result.php?keyword={q}&search_send=1'
    encoded_query = urllib.parse.quote(keyword)
    url = url.format(q=encoded_query)
    browser.get(url)
    time.sleep(0.5)
    bsoup = BeautifulSoup(browser.page_source, 'html.parser')

    product = bsoup.find('div', {'class', 'product'})
    if not product:
        return atable
    
    listarea = product.find('div', {'class', 'listarea'})
    pinfo_list = listarea.find_all('div', {'class', 'pinfo'})

    for pinfo in pinfo_list:
        name = pinfo.find('div', {'class', 'name'}).get_text()
        price = pinfo.find('div', {'class', 'price'})
        op = price.find('div', {'class': 'op'})
        op_val = int(op.get_text()) if op else None
        quantity = 1  # 假設單支
        if '6支' in name or '六支' in name:
            quantity = 6
        atable.append({
            'name': name,
            'store': '9x9',
            'price_total': op_val,
            'quantity': quantity,
            'price_unit': op_val / quantity if op_val else None
        })
    return atable

# 模擬其他的網站(momo)
def crawl_momo(keyword):
    return [
        {'name': 'Cross Window 原子筆 6支組', 'store': 'Momo', 'price_total': 600, 'quantity': 6, 'price_unit': 100},
        {'name': 'Pilot 自動原子筆', 'store': 'Momo', 'price_total': 250, 'quantity': 1, 'price_unit': 250}
    ]

def get_compare_data(keyword):
    # 在網頁執行時
    service = Service(r"C:\MyProject\webapp\driver\chromedriver-win64.exe")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    browser = webdriver.Chrome(service=service, options=options)
    
    try:
        atable = crawl_9x9(browser, keyword)
        momo = crawl_momo(keyword)
        combined = atable + momo

        # 將同類商品整理到字典
        products = {}
        for item in combined:
            key = item['name'].split()[0]
            if key not in products:
                products[key] = []
            products[key].append(item)
        return products
    finally:
        browser.quit()

# 主函式 (利用 cmd 執行時)
if __name__ == '__main__':
    keyword = "原子筆"
    products = get_compare_data(keyword)
    for pname, items in products.items():
        print(f"\n{pname}")
        for it in items:
            print(f"{it['store']}: {it['price_unit']} / 支")
