from bs4 import BeautifulSoup
import requests

#
# def get_bitcoin_price():
#     html = requests.get('https://www.google.com/search?newwindow=1&rlz=1C1CHZN_koKR935KR935&sxsrf=ALeKk03ZW01r2SN_lsEbNM5yB-xE4sRWLw%3A1615614504567&ei=KFJMYJybIpeIr7wP5Zia6A4&q=bitcoin+%EC%8B%9C%EC%84%B8&oq=bitc&gs_lcp=Cgdnd3Mtd2l6EAMYADIJCAAQQxBGEIICMgUIABCxAzIKCAAQsQMQgwEQQzIHCAAQsQMQQzIECAAQQzIFCAAQsQMyBAgAEEMyBAgAEEMyBAgAEEMyBAgAEEM6BQgAELADOgQIIxAnOgIIADoICAAQsQMQgwFQsfcCWMD7AmDNkgNoA3AAeACAAWKIAdADkgEBNZgBAKABAaoBB2d3cy13aXrIAQHAAQE&sclient=gws-wiz', headers={'User-Agent': 'Mozilla/5.0'})
#
#     html = BeautifulSoup(html.text, 'html.parser')
#     tags = html.select("div.BNeawe.iBp4i.AP7Wnd")
#     for tag in tags:
#         print(tag.text)
#
#     return tags[0].text.split(' ')[0]


import os
os.system('pip install --upgrade selenium')

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_bitcoin_price():

    ret_data = -1

    with webdriver.Chrome() as driver:
        wait = WebDriverWait(driver,15)
        url = 'https://www.google.com/search?newwindow=1&rlz=1C1CHZN_koKR935KR935&sxsrf=ALeKk03ZW01r2SN_lsEbNM5yB-xE4sRWLw%3A1615614504567&ei=KFJMYJybIpeIr7wP5Zia6A4&q=bitcoin+%EC%8B%9C%EC%84%B8&oq=bitc&gs_lcp=Cgdnd3Mtd2l6EAMYADIJCAAQQxBGEIICMgUIABCxAzIKCAAQsQMQgwEQQzIHCAAQsQMQQzIECAAQQzIFCAAQsQMyBAgAEEMyBAgAEEMyBAgAEEMyBAgAEEM6BQgAELADOgQIIxAnOgIIADoICAAQsQMQgwFQsfcCWMD7AmDNkgNoA3AAeACAAWKIAdADkgEBNZgBAKABAaoBB2d3cy13aXrIAQHAAQE&sclient=gws-wiz'
        driver.get(url)

        try:

            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.card-section.PZPZlf > div:nth-child(2) > span.pclqee"))
            )

            print(element.text)
            ret_data = element.text

        except Exception as e:
            print("Error")

    return ret_data