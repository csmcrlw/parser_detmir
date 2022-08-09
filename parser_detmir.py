from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup
from time import sleep
import re
import json
from random import randrange

browser = Chrome()
url = 'https://www.detmir.ru/catalog/index/name/lepki/'
browser.get(url)
button = browser.find_element(By.XPATH, '//*[@id="app-container"]/div[2]/main/div/div/div[2]/div/div[2]/div/button')

try:
    while button:
        button.click()
        sleep(3)
except StaleElementReferenceException:
    print('The end of the page')
finally:
    soup = BeautifulSoup(browser.page_source, features="html.parser")


urls = []
for tag_a in soup.find_all('a'):
    link = tag_a['href']
    if re.match(r'https://www.detmir.ru/product/index/id/\d*/', link):
        urls.append(link)

result_list = []
for url1 in urls:
    browser.get(url1)
    soup1 = BeautifulSoup(browser.page_source, features='html.parser')

    try:
        item_id = [i for i in url1 if i.isdigit()]
        item_id = ''.join(item_id)
    except Exception as _ex:
        item_id = None

    try:
        item_name = soup1.find('h1', class_='qY.qZ').text
    except Exception as _ex:
        item_name = None

    try:
        item_reg_price = soup1.find('span', class_='RG').text
    except Exception as _ex:
        item_reg_price = None

    try:
        item_promo_price = soup1.find('div', class_='RE').text
    except Exception as _ex:
        item_reg_price = None

    result_list.append(
        {
            'id': item_id,
            'title': item_name,
            'price': item_reg_price,
            'promo_price': item_promo_price,
            'url': url1
        }
    )

    sleep(randrange(2, 5))

with open('result_file.json', 'w') as file:
    json.dump(result_list, file, indent=4, ensure_ascii=False)
# soup_names = soup.find_all('p', class_='M_1')
# soup_reg_price = soup.find_all('span', class_='Ne')
# soup_promo_price = soup.find_all('p', class_='Nc')
# soup_city = soup.find_all('span', class_='pe')
#
#
# def get_price(ls):
#     new_ls = []
#     for price in ls:
#         pr = [pr for pr in price if pr.isdigit()]
#         new_ls.append(''.join(pr))
#     return new_ls
#
# def get_ids():
#     ids = []
#     for link in urls:
#         idd = [i for i in link if i.isdigit()]
#         ids.append(''.join(idd))
#     return ids
#
# def get_items_list(ls):
#
#     new_ls = []
#     for item in ls:
#         item_name = item.text.strip()
#         new_ls.append(item_name)
#
#     return new_ls
#
#
