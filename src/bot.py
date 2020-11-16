class ShoppingBotInterface:

    def __init__(self, config):
        """Creates a new shopping bot."""
        pass

    def check_can_buy(self, url) -> bool:
        """Checks whether or not the item is available to purchase."""
        pass

    def perform_purchase(self, url, test=False) -> bool:
        """
        Purchases the specified item.
        Returns true if purchased successfully.
        """
        pass

    def test_perform_purchase(self, url) -> bool:
        """
        Tests the execution of the perform purchase function without actually
        making a purchase.
        :param url: The url of the purchase.
        :return:
        """
        success = self.perform_purchase(url, test=True)
        if success:
            print("Passed.")
            return True
        else:
            print("Failed: An exception was thrown.")
            return False

