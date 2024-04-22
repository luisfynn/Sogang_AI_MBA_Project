from bs4 import BeautifulSoup
import requests

import os
os.system('pip install --upgrade selenium')

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_us_stock_price(company):

    ret_data = -1

    with webdriver.Chrome() as driver:
        wait = WebDriverWait(driver,15)
        url = 'https://www.google.com/search?q=' + company + 'stock'
        driver.get(url)

        try:

            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.wGt0Bc > div.PZPZlf > span:nth-child(1) > span > span.IsqQVc.NprOob.wT3VGc"))
            )

            print(element.text)
            ret_data = element.text

        except Exception as e:
            print("Error")

    return ret_data