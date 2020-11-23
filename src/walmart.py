from selenium import webdriver
from selenium.webdriver.support.ui import Select
from requests_html import HTMLSession, AsyncHTMLSession
import time
import us

from bot import ShoppingBotInterface

# import config

# Reference: http://www.michaelfxu.com/tools%20and%20infrastructures/building-a-sniping-bot/
# Bypassing Captcha: https://stackoverflow.com/questions/33225947/can-a-website-detect-when-you-are-using-selenium-with-chromedriver

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

class WalmartBot(ShoppingBotInterface):

    def __init__(self, config):
        self.config = config

    def check_can_buy(self, url) -> bool:
        try:
            session = HTMLSession()

            try:
                r = session.get(url)

                buy_btn = r.html.find(
                    'button',
                    containing='Add to cart',
                    first=True)
            finally:
                session.close()

            return buy_btn is not None

        except Exception as e:
            print("Unable to connect. Waiting 1 minute.")
            time.sleep(60)
            return False

    def perform_purchase(self, url, test=False) -> bool:
        driver = webdriver.Chrome('../chromedrivercopy.exe')
        try:
            driver.get(url)

            time.sleep(2)

            # add to cart
            add_cart_btn = driver.find_element_by_xpath(
                '//button[@class="button spin-button prod-ProductCTA--primary button--primary"]')
            if add_cart_btn == None:
                print('Product not available, DONE')
                driver.quit()
                return

            add_cart_btn.click()
            print("Added to cart.")

            # go to checkout
            time.sleep(2)

            checkout_btn = driver.find_element_by_xpath(
                '//button[@class="button ios-primary-btn-touch-fix hide-content-max-m checkoutBtn button--primary"]')

            checkout_btn.click()

            time.sleep(2)

            # continue to payment information
            continue_without_acct_btn = driver.find_element_by_xpath(
                '//button[@class="button m-margin-top width-full button--primary"]')

            continue_without_acct_btn.click()

            time.sleep(2)

            # continue to delivery
            continue_to_delivery_btn = driver.find_element_by_xpath(
                '//button[@class="button cxo-continue-btn button--primary"]')

            continue_to_delivery_btn.click()

            time.sleep(2)

            # fill in delivery information
            driver.find_element_by_id('firstName')\
                .send_keys(self.config.FIRST_NAME)
            driver.find_element_by_id('lastName')\
                .send_keys(self.config.LAST_NAME)
            driver.find_element_by_id('addressLineOne')\
                .send_keys(self.config.ADDRESS)
            driver.find_element_by_id('phone').send_keys(self.config.PHONE)
            driver.find_element_by_id('city').clear()
            driver.find_element_by_id('city').send_keys(self.config.CITY)

            drpState = Select(driver.find_element_by_id('state'))
            state = us.states.lookup(self.config.STATE)
            drpState.select_by_visible_text(state.name)

            driver.find_element_by_id('postalCode').clear()
            driver.find_element_by_id('postalCode')\
                .send_keys(self.config.ZIPCODE)
            driver.find_element_by_id('email').send_keys(self.config.EMAIL)

            notification_box = driver.find_element_by_xpath(
                '//input[@class="input-toggle__input"]')
            notification_box.click()

            print("Entered delivery information.")

            time.sleep(2)

            # continue to payment
            continue_to_payment_btn = driver.find_element_by_xpath(
                '//button[@class="button button--primary"]')

            continue_to_payment_btn.click()

            driver.find_element_by_id('firstName').clear()
            driver.find_element_by_id('firstName')\
                .send_keys(self.config.FIRST_NAME)

            driver.find_element_by_id('lastName').clear()
            driver.find_element_by_id('lastName')\
                .send_keys(self.config.LAST_NAME)

            time.sleep(1000)

            driver.find_element_by_id('creditCard').clear()
            driver.find_element_by_id('creditCard')\
                .send_keys(self.config.CREDIT_NUMBER)

            drpExpMonth = Select(driver.find_element_by_id('month-chooser'))
            drpExpMonth.select_by_visible_text(self.config.EXP_MONTH)

            drpExpYear = Select(driver.find_element_by_id('year-chooser'))
            drpExpYear.select_by_visible_text(self.config.EXP_YEAR[2:4])

            driver.find_element_by_id('cvv').clear()
            driver.find_element_by_id('cvv').send_keys(self.config.CVV)

            driver.find_element_by_id('phone').clear()
            driver.find_element_by_id('phone').send_keys(self.config.PHONE)

            print("Entered payment information.")

            # continue to review order
            driver.find_element_by_class_name('persistent-footer-continue')\
                .click()

            place_order = \
                driver.find_element_by_class_name('persistent-footer-continue')

            print("Ready to order.")

            if not test:
                place_order.click()
                print("Order placed.")

            time.sleep(50000)  # Let the user actually see something!

            return True

        except Exception as e:
            print(e)
            print("Unable to purchase.")
            return False

        finally:
            driver.quit()


def test_check_can_buy(bot):
    is_available1 = bot.check_can_buy(playstation4_url)
    is_available2 = bot.check_can_buy(playstation5_url)

    print(f"Play Station 4 is in stock: {is_available1}")
    print(f"Play Station 5 is in stock: {is_available2}")


# define main

def main():
    import config
    bot = WalmartBot(config)
    if bot.check_can_buy(specific_url):
        print(f"Executing purchase for {specific_url} ...")
        bot.perform_purchase(specific_url, test=True)
    else:
        print(f"Purchase was not executed for {specific_url}")


if __name__ == "__main__":
    main()
