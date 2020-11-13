from selenium import webdriver
from selenium.webdriver.support.ui import Select
from requests_html import HTMLSession, AsyncHTMLSession
import time

import config

# Reference: http://www.michaelfxu.com/tools%20and%20infrastructures/building-a-sniping-bot/

'''
python bot.py --name="North Face"
'''

base_url = 'https://bestbuy.com'
playstation4_url = 'https://www.bestbuy.com/site/sony-playstation-4-pro-console-jet-black/5388900.p?skuId=5388900'
playstation5_url = 'https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149'

specific_url = playstation4_url


def check_available(url):
    buy_btn = url.html.find(
        'button[class="btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button"]',
        first=True)
    return buy_btn is not None


def main():
    session = HTMLSession()
    url = session.get(specific_url)

    is_available = check_available(url)

    print(is_available)


if __name__ == "__main__":
    main()