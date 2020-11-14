from selenium import webdriver
from selenium.webdriver.support.ui import Select
from requests_html import HTMLSession, AsyncHTMLSession
import time
import threading

import config

# Reference: http://www.michaelfxu.com/tools%20and%20infrastructures/building-a-sniping-bot/

'''
python bestbuy.py --name="Play Station 5"
'''

base_url = 'https://bestbuy.com'
playstation4_url = 'https://www.bestbuy.com/site/sony-playstation-4-pro-console-jet-black/5388900.p?skuId=5388900'
playstation5_url = 'https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149'

charging_cable_url = 'https://www.bestbuy.com/site/apple-3-3-usb-type-c-to-lightning-charging-cable-white/6259804.p?skuId=6259804'


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
    session = HTMLSession()

    try:
        r = session.get(url)

        buy_btn = r.html.find(
            'button[class="btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button"]',
            first=True)
    finally:
        session.close()

    return buy_btn is not None


def perform_purchase(url, test=True):
    '''
    Given url of product, add to cart then checkout
    '''
    driver = webdriver.Chrome('chromedriver.exe')
    try:
        driver.get(url)
        btn = driver.find_element_by_class_name('add-to-cart-button')
        # if len(btn) == 0:
        #     print('not available, DONE')
        #     return

        btn.click()
        time.sleep(1)

        print("Successfully added to cart.")

        checkout_url = 'https://www.bestbuy.com/checkout/r/fulfillment'
        driver.get(checkout_url)

        # if we are currently on store pickup, switch to shipping
        try:
            shipping_button = driver.find_element_by_class_name('ispu-card__switch')\
                .find_element_by_tag_name('a')
            shipping_button.click()
            print("Switching to shipping")
        except Exception as e:
            print("Started on shipping page.")

        # fill in general info and shipping info
        driver.find_element_by_xpath("//input[contains(@id,'firstName')]") \
            .send_keys(config.FIRST_NAME)
        driver.find_element_by_xpath("//input[contains(@id,'lastName')]") \
            .send_keys(config.LAST_NAME)
        driver.find_element_by_xpath("//input[contains(@id,'street')]") \
            .send_keys(config.ADDRESS)
        time.sleep(0.5)
        driver.find_element_by_xpath("//input[contains(@id,'city')]") \
            .send_keys(config.CITY)

        drpState = \
            Select(driver.find_element_by_xpath(
                "//select[contains(@id,'state')]"))
        # if drpState is None:
        #     print("Unable to enter shipping address.")
        #     return
        drpState.select_by_visible_text(config.STATE)

        driver.find_element_by_xpath("//input[contains(@id,'zipcode')]") \
            .send_keys(config.ZIPCODE)

        driver.find_element_by_id('user.emailAddress').send_keys(config.EMAIL)
        driver.find_element_by_id('user.phone').send_keys(config.PHONE)

        print("Successfully filled out general info and shipping.")

        # move on to payment info
        continue_button = driver.find_element_by_class_name('btn-secondary')
        # if len(continue_button) == 0:
        #     print("Unable to continue to payment info.")
        #     return
        continue_button.click()
        print("Continuing to payment info.")

        time.sleep(5)

        # fill in payment info
        driver.find_element_by_id('optimized-cc-card-number') \
            .send_keys(config.CREDIT_NUMBER)

        exp_month = Select(driver.find_element_by_name('expiration-month'))
        # if exp_month is None:
        #     print("Unable to enter credit card expiration month.")
        #     return
        exp_month.select_by_visible_text(config.EXP_MONTH)

        exp_year = Select(driver.find_element_by_name('expiration-year'))
        # if exp_year is None:
        #     print("Unable to enter credit card expiration year.")
        #     return
        exp_year.select_by_visible_text(config.EXP_YEAR)

        driver.find_element_by_id('credit-card-cvv').send_keys(config.CVV)

        print("Successfully entered credit card information.")

        # # enter billing address
        # driver.find_element_by_id('payment.billingAddress.firstName') \
        #     .send_keys(config.FIRST_NAME)
        # driver.find_element_by_id('payment.billingAddress.lastName') \
        #     .send_keys(config.LAST_NAME)
        # driver.find_element_by_id('payment.billingAddress.street') \
        #     .send_keys(config.ADDRESS)
        # driver.find_element_by_id('payment.billingAddress.city') \
        #     .send_keys(config.CITY)
        #
        # state_menu = Select(
        #     driver.find_element_by_id('payment.billingAddress.state'))
        # # if state_menu is None:
        # #     print("Unable to enter billing state.")
        # #     return
        # state_menu.select_by_visible_text(config.STATE)
        #
        # driver.find_element_by_id('payment.billingAddress.zipcode') \
        #     .send_keys(config.ZIPCODE)
        #
        # print("Successfully entered billing address.")

        # Place the order
        place_order = driver.find_element_by_class_name('btn-block')
        # if len(place_order) == 0:
        #     print("Unable to place order.")
        #     return

        if not test:
            place_order.click()
        print("Order placed.")

    except Exception as e:
        print(e)

    finally:
        driver.quit()


def test_check_can_buy(url):
    is_available = check_can_buy(url)
    print(is_available)


def test_perform_purchase(url):
    perform_purchase(url, test=True)


def main():
    threads = []
    url = playstation5_url
    test = False

    available = check_can_buy(url)
    while not available:
        available = check_can_buy(url)
        print("Unavailable. Waiting 10 seconds.")
        time.sleep(10)

    # start the threads
    for i in range(config.NUM_BUY):
        x = threading.Thread(target=perform_purchase, args=(url, test))
        x.start()
        threads.append(x)

    # wait for the threads to stop
    for thread in threads:
        thread.join()

    # import argparse
    # parser = argparse.ArgumentParser(description='PS5 bot main parser')
    # parser.add_argument('--name', required=True,
    #                     help='Specify product name to find and purchase')
    # args = parser.parse_args()
    # print(args.name)
    # main_(target_product=args.name)


if __name__ == "__main__":
    main()
