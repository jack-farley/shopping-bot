from selenium import webdriver
from selenium.webdriver.support.ui import Select
from requests_html import HTMLSession
import time

from bot import ShoppingBotInterface

# Reference: http://www.michaelfxu.com/tools%20and%20infrastructures/building-a-sniping-bot/
'''
python bestbuy.py --name="Play Station 5"
'''


class BestBuyBot(ShoppingBotInterface):

    def __init__(self, config):
        self.config = config

    def check_can_buy(self, url) -> bool:
        try:
            session = HTMLSession()
            try:
                r = session.get(url)
                btn = r.html.find('button[class="btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button"]')

                return len(btn) == 1

            finally:
                session.close()

        except Exception as e:
            print("Unable to connect. Waiting 1 minute.")
            time.sleep(60)
            return False

    def perform_purchase(self, url, test=False) -> bool:
        driver = webdriver.Chrome('../chromedriver.exe')
        try:
            driver.get(url)
            btn = driver.find_element_by_class_name('add-to-cart-button')

            btn.click()
            time.sleep(1)

            print("Successfully added to cart.")

            checkout_url = 'https://www.bestbuy.com/checkout/r/fulfillment'
            driver.get(checkout_url)

            # if we are currently on store pickup, switch to shipping
            try:
                shipping_button = driver.find_element_by_xpath("//a[class='ispu-card__switch']")
                shipping_button.click()
                print("Switching to shipping")
            except Exception as e:
                print("Started on shipping page.")

            # fill in general info and shipping info
            driver.find_element_by_xpath("//input[contains(@id,'firstName')]") \
                .send_keys(self.config.FIRST_NAME)
            driver.find_element_by_xpath("//input[contains(@id,'lastName')]") \
                .send_keys(self.config.LAST_NAME)
            driver.find_element_by_xpath("//input[contains(@id,'street')]") \
                .send_keys(self.config.ADDRESS)
            time.sleep(0.5)
            driver.find_element_by_xpath("//input[contains(@id,'city')]") \
                .send_keys(self.config.CITY)

            drpState = Select(driver.find_element_by_xpath(
                "//select[contains(@id,'state')]"))
            drpState.select_by_visible_text(self.config.STATE)

            driver.find_element_by_xpath("//input[contains(@id,'zipcode')]") \
                .send_keys(self.config.ZIPCODE)

            driver.find_element_by_id('user.emailAddress').send_keys(
                self.config.EMAIL)
            driver.find_element_by_id('user.phone') \
                .send_keys(self.config.PHONE)

            print("Successfully filled out general info and shipping.")

            # move on to payment info
            continue_button = driver.find_element_by_class_name(
                'btn-secondary')
            continue_button.click()
            print("Continuing to payment info.")

            time.sleep(5)

            # fill in payment info
            driver.find_element_by_id('optimized-cc-card-number') \
                .send_keys(self.config.CREDIT_NUMBER)

            exp_month = Select(driver.find_element_by_name('expiration-month'))
            exp_month.select_by_visible_text(self.config.EXP_MONTH)

            exp_year = Select(driver.find_element_by_name('expiration-year'))
            exp_year.select_by_visible_text(self.config.EXP_YEAR)

            driver.find_element_by_id('credit-card-cvv') \
                .send_keys(self.config.CVV)

            print("Successfully entered credit card information.")

            # Place the order
            place_order = driver.find_element_by_class_name('btn-block')

            print("Ready to place order.")

            if not test:
                place_order.click()
                print("Order placed.")
            return True

        except Exception as e:
            print(e)
            print("Unable to purchase.")
            return False

        finally:
            driver.quit()
