
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
test_url = 'https://www.walmart.com/ip/onn-True-Wireless-Earphones-White/283162082'

specific_url = test_url


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

        time.sleep(2)

        add_cart_btn = driver.find_element_by_xpath(
            '//button[@class="button spin-button prod-ProductCTA--primary button--primary"]')
        if add_cart_btn == None:
            print('Product not available, DONE')
            driver.quit()
            return

        add_cart_btn.click()

        time.sleep(2)

        checkout_btn = driver.find_element_by_xpath(
            '//button[@class="button ios-primary-btn-touch-fix hide-content-max-m checkoutBtn button--primary"]')

        checkout_btn.click()

        time.sleep(2)

        continue_without_acct_btn = driver.find_element_by_xpath(
            '//button[@class="button m-margin-top width-full button--primary"]')

        continue_without_acct_btn.click()

        time.sleep(2)

        continue_to_delivery_btn = driver.find_element_by_xpath(
            '//button[@class="button cxo-continue-btn button--primary"]')

        continue_to_delivery_btn.click()

        time.sleep(2)

        driver.find_element_by_id('firstName').send_keys('John')
        driver.find_element_by_id('lastName').send_keys('Doe')
        driver.find_element_by_id(
            'addressLineOne').send_keys('123 Broadway Ave')
        driver.find_element_by_id('phone').send_keys('8571234567')
        driver.find_element_by_id('city').clear()
        driver.find_element_by_id('city').send_keys('Boston')
        driver.find_element_by_id('state').send_keys('Massachusetts')
        driver.find_element_by_id('postalCode').clear()
        driver.find_element_by_id('postalCode').send_keys('02101')
        driver.find_element_by_id('email').send_keys('jdoe123@gmail.com')

        notification_box = driver.find_element_by_xpath(
            '//input[@class="input-toggle__input"]')
        notification_box.click()

        time.sleep(2)

        continue_to_payment_btn = driver.find_element_by_xpath(
            '//button[@class="button button--primary"]')

        continue_to_delivery_btn.click()

        time.sleep(50000)  # Let the user actually see something!
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
