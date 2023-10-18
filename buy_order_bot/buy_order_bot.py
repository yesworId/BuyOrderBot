from steampy.client import SteamClient
from steampy.models import Currency
from steampy.utils import GameOptions
import steampy.exceptions

import os
import re
import csv
import json
import decimal

from time import sleep


def are_credentials_filled(config_file) -> bool:
    with open(config_file) as file:
        config = json.load(file)
        return all(config.values())


class SteamBot:
    def __init__(self, config_file, steam_guard_file, items_file):
        with open(config_file) as file:
            config = json.load(file)

        self.api_key = config['api_key']
        self.username = config['username']
        self.password = config['password']
        self.currency = config['currency']
        self.steam_guard = steam_guard_file
        self.items_file = items_file

        self.cookies = self.get_cookies()
        self.proxies = self.get_proxies()

        self.steam_client = SteamClient(
            api_key=self.api_key,
            username=self.username,
            password=self.password,
            steam_guard=self.steam_guard,
            login_cookies=self.cookies,
            proxies=self.proxies)

        self.balance = None
        self.buy_order_limit = None
        self.total_cost = None

        self.ordered_items_dict = {}
        self.items_list = []

    @staticmethod
    def get_cookies():
        if os.path.exists('cookies.json'):
            with open('cookies.json', 'r', encoding='utf-8') as cookies_file:
                return json.load(cookies_file)
        else:
            return None

    @staticmethod
    def get_proxies():
        if os.path.exists('proxies.json'):
            with open('proxies.json') as proxies_file:
                return json.load(proxies_file)
        else:
            return None

    def login_required(func):
        def func_wrapper(self, *args, **kwargs):
            if self.steam_client.is_session_alive() is not True:
                print("Login method was not used.  Attempting to log in...")
                self.login()
            return func(self, *args, **kwargs)
        return func_wrapper

    def login(self):
        """
        Authorizing into a Steam account using the provided credentials and Steam Guard.
        Returns an instance of the SteamClient after successful authorization.
        """
        try:
            self.steam_client.login()
            print(f"Successfully Logged in {self.username}")
        except steampy.exceptions.InvalidCredentials:
            print("Wrong credentials.")
            exit(1)
        except steampy.exceptions.CaptchaRequired:
            print("Captcha appeared try again later.")
            exit(1)
        except Exception as ex:
            print(f"Failed to login into account: {str(ex)}")
            exit(1)

        return self.steam_client

    @login_required
    def initialize_account_balance(self):
        """
        Getting account balance and Buy Order limit.
        """
        try:
            # Initialize and print account balance
            self.balance = self.steam_client.get_wallet_balance()
            print(f"Balance: {self.balance} {self.currency}")

            # Initialize BuyOrder limit (10 * balance)
            self.buy_order_limit = 10 * self.balance

            return self.balance, self.buy_order_limit
        except Exception as ex:
            print(f"Failed to initialize account balance: {str(ex)}")
            exit(1)

    @login_required
    def get_buy_order_listings(self):
        """
        Getting active BuyOrder listings.
        Calculating available BuyOrder limit.
        """

        # Get all market listings
        market_listings = self.steam_client.market.get_my_market_listings()

        # Get only Buy order listings
        buy_listings = market_listings.get("buy_orders")

        if buy_listings:
            self.total_cost = decimal.Decimal(0)  # Initialize as Decimal
            for listing_id, listing_info in buy_listings.items():
                item_name = listing_info["item_name"]

                # Update "price" value (get rid of currency symbol)
                price = re.sub(r'[^\d.,]', '', listing_info["price"])
                price = price.replace(',', '.')
                quantity = listing_info["quantity"]
                self.total_cost += decimal.Decimal(price) * quantity  # Convert to Decimal

                self.ordered_items_dict[item_name] = {
                    "name": item_name,
                    "price": price,
                    "quantity": quantity
                }

            return self.total_cost, self.ordered_items_dict

        else:
            print("No buy orders found.")
            self.total_cost = decimal.Decimal(0)
            return self.total_cost, self.ordered_items_dict  # Return Decimal(0) when no buy orders found

    def read_items_from_csv(self):
        """
        Read items from a CSV file and return a list of tuples containing item_name, item_price, and item_amount.
        """
        with open(self.items_file, newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                item_name, item_price, item_amount = row
                self.items_list.append((item_name, decimal.Decimal(item_price), int(item_amount)))
        return self.items_list

    @login_required
    def create_buy_order(self, item_name, item_price, item_amount):
        """
        Creating Buy Order for a single item.
        """
        try:
            item_price = int(item_price * 100)
            response = self.steam_client.market.create_buy_order(item_name, item_price, item_amount,
                                                                 GameOptions.CS, Currency[self.currency])
            print(f"BuyOrder created for item '{item_name}' with BuyOrder ID: {response['buy_orderid']}")
            return True
        except Exception as ex:
            print(f"Failed to create order for item '{item_name}': {str(ex)}")
            sleep(1)
            return False

    @login_required
    def place_buy_orders_for_items(self):
        """
        Placing Buy Order for items from items.csv file
        """

        # Read items from the CSV file and store them in a list
        self.items_list = self.read_items_from_csv()

        # Continue while there are items without BuyOrders
        while any(item[0] not in self.ordered_items_dict for item in self.items_list):
            for item_name, item_price, item_amount in self.items_list:
                if item_name in self.ordered_items_dict:
                    continue

                # Check if enough funds for Buy Order
                if decimal.Decimal(item_price) > self.balance:
                    print(f"Price for item '{item_name} is higher than balance'")
                    continue

                # Check if the balance exceeds
                if decimal.Decimal(item_price) * item_amount > self.balance:
                    print(f"BuyOrder for item '{item_name}' exceeds balance")
                    continue

                # Check if the buy order limit exceeds
                if decimal.Decimal(item_price) * item_amount > self.buy_order_limit:
                    print(f"BuyOrder for item '{item_name}' exceeds BuyOrder limit")
                    continue

                # Place the buy order for the item
                if self.create_buy_order(item_name, item_price, item_amount):
                    self.ordered_items_dict[item_name] = {
                        'name': item_name,
                        'price': item_price,
                        'quantity': item_amount,
                    }
                    self.buy_order_limit -= decimal.Decimal(item_price) * item_amount
                    print(f"BuyOrder limit: {self.buy_order_limit:.2f} {self.currency}")

        print("Finished processing of all items.")

    @login_required
    def save_cookies(self):
        try:
            with open('cookies.json', 'w', encoding='utf-8') as cookies_file:
                json.dump(self.steam_client._session.cookies.get_dict(), cookies_file)
                print("Saved cookies")
        except Exception as ex:
            print(f"Couldn't save cookies: {ex}")

    def main(self):

        config_file = 'config.json'

        if not are_credentials_filled(config_file):
            print('Please fill missing credentials in config.json')
            exit(1)

        self.save_cookies()

        self.initialize_account_balance()

        self.get_buy_order_listings()

        # Calculate and print available buy order limit
        self.buy_order_limit -= self.total_cost
        if self.buy_order_limit > 0:
            print(f"Available Buy Order Limit: {self.buy_order_limit} {self.currency}")
        else:
            print(f"Sum of active orders exceeds balance: {self.buy_order_limit} {self.currency}")

        self.place_buy_orders_for_items()


bot = SteamBot(config_file='config.json', steam_guard_file='steam_guard.json', items_file='items.csv')
bot.main()
