import time
import threading

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


def watch(bot, url):
    print("Watching: " + url)
    checks = 0
    available = bot.check_can_buy(url)
    while not available:
        checks = checks + 1
        print("Unavailable. Waiting 10 seconds. Iteration "
              + str(checks) + ".")
        time.sleep(10)
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


def main():
    bestbuy = BestBuyBot(config)

    url = bestbuy_playstation5_url

    watch(bestbuy, url)

    buy(bestbuy, url, 4, test=False)

    return

    # import argparse
    # parser = argparse.ArgumentParser(description='PS5 bot main parser')
    # parser.add_argument('--name', required=True,
    #                     help='Specify product name to find and purchase')
    # args = parser.parse_args()
    # print(args.name)
    # main_(target_product=args.name)


if __name__ == "__main__":
    main()
