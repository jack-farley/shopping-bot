from selenium import webdriver
from selenium.webdriver.support.ui import Select
from requests_html import HTMLSession, AsyncHTMLSession
import time

# import config

# Reference: http://www.michaelfxu.com/tools%20and%20infrastructures/building-a-sniping-bot/

'''
python walmart.py
'''

base_url = 'https://www.walmart.com/'
playstation4_url = 'https://www.walmart.com/ip/Sony-PlayStation-4-1TB-Slim-Gaming-Console/101507200'
playstation5_url = 'https://www.walmart.com/ip/PlayStation-5-Console/363472942'

specific_url = playstation4_url


# def get_product_links():
#     '''
#     Returns list of elements "items",
#     each containing a link to product detail page
#     '''
#     pass


# def get_matched_and_available(target_name):
#     '''
#     Given a target name, filter the product on main page,
#     and return links to products with available items

#     checked_urls: if already checked (and not a match in product name),
#     skip in future checks

#     Exactly how this should work, depends on how the drop works - is the page already there,
#     just not for sale yet? Or page is added at drop time?
#     '''
#     pass


def check_can_buy(url):
    '''
    Given a page (returned by session.get(target_url)),
    find if there is such html code within:
    <input type="submit" name="commit" value="add to cart" class="button">
    Returns True if so, False if not
    '''
    session = HTMLSession()
    response = session.get(url)
    buy_btn = response.html.find(
        'button',
        containing='Add to cart', first=True)

    return buy_btn is not None


def perform_purchase(url):
    '''
    Given url of product, add to cart then checkout
    '''
    try:
        driver = webdriver.Chrome('chromedriver.exe')
        driver.get(url)

        btn = driver.find_element_by_class_name('hello_world')
        if btn == None:
            print('Product not available, DONE')
            driver.quit()
            return

        btn[0].click()

        time.sleep(5)  # Let the user actually see something!
        driver.quit()
    except Exception as e:
        print(e)


def test_check_can_buy():
    is_available1 = check_can_buy(playstation4_url)
    is_available2 = check_can_buy(playstation5_url)

    print(f"Play Station 4 is in stock: {is_available1}")
    print(f"Play Station 5 is in stock: {is_available2}")


# define main

def main():
    if(check_can_buy(specific_url)):
        print(f"Executing purchase for {specific_url} ...")
        perform_purchase(specific_url)
    else:
        print(f"Purchase was not executed for {specific_url}")


if __name__ == "__main__":
    main()
