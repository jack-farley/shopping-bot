from selenium import webdriver
from selenium.webdriver.support.ui import Select
from requests_html import HTMLSession, AsyncHTMLSession
import time

#import config

'''
python bot.py --name="Play Station"
'''


def get_product_links():
    pass


def get_matched_and_available(target_name):
    pass


def check_can_buy(r):
    pass


def perform_purchase(url):
    pass


def main(target_product):
    pass


# define main
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Supremebot main parser')
    parser.add_argument('--name', required=True,
                        help='Specify product name to find and purchase')
    args = parser.parse_args()
    main(target_product=args.name)
