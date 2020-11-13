from selenium import webdriver
from selenium.webdriver.support.ui import Select
from requests_html import HTMLSession, AsyncHTMLSession
import time

#import config

'''
python bot.py --name="Play Station"
'''


def get_product_links():
    '''
    Returns list of elements "items",
    each containing a link to product detail page
    '''
    pass


def get_matched_and_available(target_name):
    '''
    Given a target name, filter the product on main page,
    and return links to products with available items

    checked_urls: if already checked (and not a match in product name),
    skip in future checks

    Exactly how this should work, depends on how the drop works - is the page already there,
    just not for sale yet? Or page is added at drop time?
    '''
    pass


def check_can_buy(r):
    '''
    Given a page (returned by session.get(target_url)),
    find if there is such html code within:
    <input type="submit" name="commit" value="add to cart" class="button">
    Returns True if so, False if not
    '''
    pass


def perform_purchase(url):
    '''
    Given url of product, add to cart then checkout
    '''
    pass


def main(target_product):
    pass


# define main
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='PS5 bot main parser')
    parser.add_argument('--name', required=True,
                        help='Specify product name to find and purchase')
    args = parser.parse_args()
    print(args.name)
    main(target_product=args.name)
