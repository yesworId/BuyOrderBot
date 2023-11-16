from steampy.client import SteamClient
from steampy.models import Currency
from steampy.utils import GameOptions
import steampy.exceptions

import os
import re
import csv
import json
from decimal import Decimal

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

        self.steam_client = None
        self.balance = None
        self.buy_order_limit = None
        self.total_cost = Decimal(0)

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
            if not self.steam_client.is_session_alive():
                print("Login method was not used.  Attempting to log in...")
                self.login()
            return func(self, *args, **kwargs)
        return func_wrapper

    def login(self):
        """
        Authorizing into Steam account using cookies and provided credentials.
        Returns an instance of the SteamClient after successful authorization.
        """
        self.steam_client = SteamClient(
            api_key=self.api_key,
            username=self.username,
            password=self.password,
            steam_guard=self.steam_guard,
            login_cookies=self.cookies,
            proxies=self.proxies)

        # Check if the session remains active after logging in with cookies.
        # If not, log in using credentials.
        if not (self.steam_client.was_login_executed and self.steam_client.is_session_alive()):

            for attempt in range(3):
                try:
                    self.steam_client.login()
                    print(f"Successfully logged in {self.username}")
                    return self.steam_client.is_session_alive()
                except steampy.exceptions.InvalidCredentials:
                    print("Wrong credentials.")
                    exit(1)
                except steampy.exceptions.CaptchaRequired:
                    print("Captcha appeared try again later.")
                    break
                except Exception as ex:
                    print(f"Failed to login into account: {str(ex)}")
                    sleep(20)

            print("Reached max login attempts. Exiting.")
            exit(1)

        else:
            print("Successfully logged in using cookies")

        return self.steam_client

    @login_required
    def initialize_account_balance(self):
        """
        Getting account balance and Buy Order limit.
        """
        while self.balance is None:
            try:
                # Initialize and print account balance
                self.balance = self.steam_client.get_wallet_balance()
                print(f"Balance: {self.balance} {self.currency}")

                # Initialize BuyOrder limit (10 * balance)
                self.buy_order_limit = 10 * self.balance

            except Exception as ex:
                print(f"Failed to initialize account balance: {str(ex)}")
                sleep(5)

        return self.balance, self.buy_order_limit

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
            for listing_id, listing_info in buy_listings.items():

                item_name = listing_info["item_name"]
                price = re.sub(r'[^\d.,]', '', listing_info["price"])  # Get rid of currency symbol
                price = price.replace(',', '.')
                quantity = listing_info["quantity"]
                self.total_cost += Decimal(price) * quantity  # Add-up the sum of every order

                self.ordered_items_dict[item_name] = {
                    "name": item_name,
                    "price": price,
                    "quantity": quantity
                }

        else:
            print("No buy orders found.")

        return self.total_cost, self.ordered_items_dict

    def read_items_from_csv(self):
        """
        Read items from a CSV file and return a list of tuples containing item_name, item_price, and item_amount.
        """
        with open(self.items_file, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                item_name, item_price, item_amount, game_name = row
                self.items_list.append((item_name, Decimal(item_price), int(item_amount), game_name.strip()))
        return self.items_list

    @login_required
    def create_buy_order(self, item_name, item_price, item_amount, game_name):
        """
        Creating Buy Order for a single item.
        """
        try:
            game = getattr(GameOptions, game_name, None)
            if game is not None:
                response = self.steam_client.market.create_buy_order(item_name, int(item_price * 100), item_amount,
                                                                     game, Currency[self.currency])
                print(f"Created Buy Order for '{item_name}' with BuyOrder ID: {response['buy_orderid']}")
                return True
            else:
                print(f"Invalid game name: {game_name} for item: {item_name}")
                return False
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
            for item_name, item_price, item_amount, game_name in self.items_list:
                if item_name in self.ordered_items_dict:
                    continue

                # Check if enough funds for Buy Order
                if Decimal(item_price) > self.balance:
                    print(f"Price for item '{item_name} is higher than balance'")
                    continue

                # Check if the balance exceeds
                if Decimal(item_price) * item_amount > self.balance:
                    print(f"BuyOrder for item '{item_name}' exceeds balance")
                    continue

                # Check if the buy order limit exceeds
                if Decimal(item_price) * item_amount > self.buy_order_limit:
                    print(f"BuyOrder for item '{item_name}' exceeds BuyOrder limit")
                    continue

                # Place Buy Order for item
                if self.create_buy_order(item_name, item_price, item_amount, game_name):
                    self.ordered_items_dict[item_name] = {
                        'name': item_name,
                        'price': item_price,
                        'quantity': item_amount,
                    }
                    self.buy_order_limit -= Decimal(item_price) * item_amount
                    print(f"BuyOrder limit: {self.buy_order_limit:.2f} {self.currency}")

        print("Finished processing of all items.")

    @login_required
    def update_cookies(self):
        try:
            with open('cookies.json', 'w', encoding='utf-8') as cookies_file:
                self.cookies = self.steam_client._session.cookies.get_dict()
                json.dump(self.cookies, cookies_file)
                print("Saved cookies")
        except Exception as ex:
            print(f"Couldn't save cookies: {ex}")

        return self.cookies

    def main(self):
        if not are_credentials_filled('config.json'):
            print('Please fill missing credentials in config.json')
            exit(1)

        self.login()

        self.update_cookies()

        self.initialize_account_balance()

        self.get_buy_order_listings()

        # Calculate and print available buy order limit
        self.buy_order_limit -= self.total_cost

        if self.buy_order_limit > 0:
            print(f"Available Buy Order Limit: {self.buy_order_limit} {self.currency}")
            self.place_buy_orders_for_items()
        else:
            print(f"Couldn't place buy orders. "
                  f"Sum of active orders exceeds balance: {self.buy_order_limit} {self.currency}")


bot = SteamBot(config_file='config.json', steam_guard_file='steam_guard.json', items_file='items.csv')
bot.main()
