import time
import threading

import config
from bestbuy import BestBuyBot

# bestbuy urls
base_url = 'https://bestbuy.com'
playstation4_url = 'https://www.bestbuy.com/site/sony-playstation-4-pro-console-jet-black/5388900.p?skuId=5388900'
playstation5_url = 'https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149'
charging_cable_url = 'https://www.bestbuy.com/site/apple-3-3-usb-type-c-to-lightning-charging-cable-white/6259804.p?skuId=6259804'


def watch(bot, url):
    print("Watching: " + url)
    checks = 0
    available = bot.check_can_buy(url)
    while not available:
        print("Unavailable. Waiting 10 seconds. Iteration "
              + str(checks) + ".")
        time.sleep(10)
        available = bot.check_can_buy(url)

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


def main():
    bestbuy = BestBuyBot(config)

    print(bestbuy.check_can_buy(charging_cable_url))
    print(bestbuy.check_can_buy(playstation5_url))
    bestbuy.test_perform_purchase(charging_cable_url)

    # import argparse
    # parser = argparse.ArgumentParser(description='PS5 bot main parser')
    # parser.add_argument('--name', required=True,
    #                     help='Specify product name to find and purchase')
    # args = parser.parse_args()
    # print(args.name)
    # main_(target_product=args.name)


if __name__ == "__main__":
    main()
