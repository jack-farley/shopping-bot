import threading
import time
import argparse

import config
from bestbuy import BestBuyBot
from walmart import WalmartBot

# bestbuy urls
bestbuy_base_url = 'https://bestbuy.com'
bestbuy_playstation4_url = 'https://www.bestbuy.com/site/sony-playstation-4-pro-console-jet-black/5388900.p?skuId=5388900'
bestbuy_playstation5_url = 'https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149'
bestbuy_charging_cable_url = 'https://www.bestbuy.com/site/apple-3-3-usb-type-c-to-lightning-charging-cable-white/6259804.p?skuId=6259804'
bestbuy_portable_charger_url = 'https://www.bestbuy.com/site/insignia-extended-play-5000-mah-portable-charger-for-nintendo-switch-lite-black/6387845.p?skuId=6387845'
bestbuy_roku_url = 'https://www.bestbuy.com/site/roku-premiere-4k-streaming-media-player-black/6293217.p?skuId=6293217'

# walmart urls
walmart_base_url = 'https://www.walmart.com/'
walmart_playstation4_url = 'https://www.walmart.com/ip/Sony-PlayStation-4-1TB-Slim-Gaming-Console/101507200'
walmart_playstation5_url = 'https://www.walmart.com/ip/PlayStation-5-Console/363472942'
walmart_test_url = 'https://www.walmart.com/ip/onn-True-Wireless-Earphones-White/283162082'


def watch(bot, url, delay):
    print("Watching: " + url)
    checks = 0
    available = bot.check_can_buy(url)
    while not available:
        checks = checks + 1
        print("Unavailable. Waiting 10 seconds. Iteration "
              + str(checks) + ".")
        time.sleep(delay)
        available = bot.check_can_buy(url)

    print("The item is available.")

    return available


def buy(bot, url, num=0, test=True):
    threads = []
    print("Buying from: " + url)
    print("Test: " + str(test))

    # start the threads
    for i in range(num):
        x = threading.Thread(target=bot.perform_purchase, args=(url, test))
        x.start()
        threads.append(x)

    # wait for the threads to stop
    for thread in threads:
        thread.join()


def get_bot(link):

    if link.find("www.bestbuy.com") != -1:
        return BestBuyBot(config)

    elif link.find("www.walmart.com") != -1:
        return WalmartBot(config)

    else:
        return None


def main():

    parser = argparse.ArgumentParser(description='A bot for online shopping.',
                                     prog='shopper', formatter_class=
                                     argparse.MetavarTypeHelpFormatter)
    parser.add_argument('url', type=str, help='the link of the item to buy')
    parser.add_argument('-d', dest='delay', type=int, default=10,
                        help='the amount of time for the bot to wait after '
                             'seeing that the item is out of stock before '
                             'checking again')
    parser.add_argument('-n', dest='number', type=int, default=1,
                        help='the number of the specified item to buy')

    args = parser.parse_args()

    url = args.url
    delay = args.delay
    number = args.number

    # buy the item

    bot = get_bot(url)

    if bot is None:
        print("Invalid link.")
        return

    if number < 1:
        print("Must purchase a positive number of the item.")
        return

    watch(bot, url, delay)

    buy(bot, url, number, test=False)

    return


if __name__ == "__main__":
    main()
