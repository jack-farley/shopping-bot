from selenium import webdriver
from selenium.webdriver.support.ui import Select
from requests_html import HTMLSession, AsyncHTMLSession
import time

# import config

# Reference: http://www.michaelfxu.com/tools%20and%20infrastructures/building-a-sniping-bot/

'''
python bestbuy.py --name="Play Station 5"
'''

base_url = 'https://www.walmart.com/'
playstation4_url = 'https://www.walmart.com/ip/Sony-PlayStation-4-1TB-Slim-Gaming-Console/101507200'
playstation5_url = 'https://www.walmart.com/ip/PlayStation-5-Console/363472942'

specific_url = playstation5_url


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


def check_can_buy(url):
    '''
    Given a page (returned by session.get(target_url)),
    find if there is such html code within:
    <input type="submit" name="commit" value="add to cart" class="button">
    Returns True if so, False if not
    '''

    buy_btn = url.html.find(
        'button',
        containing='Add to cart', first=True)
    return buy_btn is not None


def perform_purchase(url):
    '''
    Given url of product, add to cart then checkout
    '''
    pass


def test_check_can_buy():
    session = HTMLSession()
    url1 = session.get(playstation4_url)
    url2 = session.get(playstation5_url)
    is_available1 = check_can_buy(url1)
    is_available2 = check_can_buy(url2)

    print(f"Play Station 4 is in stock: {is_available1}")
    print(f"Play Station 5 is in stock: {is_available2}")


def main_(target_product):
    pass


# define main
def main():
    test_check_can_buy()

    # import argparse
    # parser = argparse.ArgumentParser(description='PS5 bot main parser')
    # parser.add_argument('--name', required=True,
    #                     help='Specify product name to find and purchase')
    # args = parser.parse_args()
    # print(args.name)
    # main_(target_product=args.name)


if __name__ == "__main__":
    main()
