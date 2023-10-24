# BuyOrderBot
This Bot is designed to automate process of placing buy orders for Steam Market items.\
If you like this project, don't forget to star it.\
I'm using [steampy](https://github.com/bukson/steampy), precious library for this bot. The author made such a good job. Thank you [bukson!](https://github.com/bukson)\
If someone has any ideas how to improve it -> feel free to share them with me.

## Features
* Placing buy orders for different items;
* Using cookies for authentication;
* Using **proxies**;
* Placing buy orders for different games: **CS2, DOTA2, RUST, TF2**;
* Prints user balance and buy order limit;

## How does it work?
* First of all, bot logs into your Steam account using cookies or provided credentials. Then it gets your account balance and calculates BuyOrder limit to compare the sum of the order ​​to it. BuyOrder limit is ten times your balance.
* Next step is to get total cost of all orders, so bot gets all of your BuyOrder listing, which still active on account for this. The program subtracts the value of the total cost from the BuyOrder limit and gets the current value of BuyOrder limit.
* After all of this, bot is ready to place buy orders. It goes through each item in your items.csv file and tries to place buy order.
* Program finishes after all items successfully got placed buy orders.

## Setup

config.json
-----------
First of all create config.json file.
* [Obtaining API key](https://steamcommunity.com/dev/apikey)
* [Choose your currency](https://github.com/YESW0RLD/BuyOrderBot/blob/master/README.md#currencies)

```json
{
  "api_key": "YOUR_API_KEY",
  "username": "YOUR_USERNAME",
  "password": "YOUR_PASSWORD",
  "currency": "YOUR_CURRENCY"
}
```

steam_guard.json
----------------

Then, you need to obtain **shared_secret** and **identity_secret** from MaFile. Save them in **steam_guard.json** file.

**Pay your attention!**
This methods are different for SDA and Steam Mobile Authenticator!

* [Obtaining MaFile from Steam Desktop Authenticator](https://github.com/SteamTimeIdler/stidler/wiki/Getting-your-%27shared_secret%27-code-for-use-with-Auto-Restarter-on-Mobile-Authentication#getting-shared-secret-from-steam-desktop-authenticator-windows)

```json
{
    "steamid": "YOUR_STEAM_ID",
    "shared_secret": "YOUR_SHARED_SECRET",
    "identity_secret": "YOUR_IDENTITY_SECRET"
  }
```
proxies.json
------------
If you have proxies, you can add them in proxies.json file.

```json
{
    "http": "http://login:password@host:port",
    "https": "http://login:password@host:port"
}
```


## Usage
You already decided which items you want to buy.

Now you need to create items.csv file where you write down all the item names with the prices and item amount you want to buy.

**Warning!**
First you must write the name of the item, then price you want to buy it for, and the amount of those items. You can set the prices at the same way as you do it on Steam Market

**Example:**
``` csv
Name, Price, Amount, Game
Snakebite Case, 1.5, 2, CS
Operation Bravo Case, 10.6, 1, CS
AK-47 | Asiimov (Field-Tested), 5.7, 1, CS
Paris 2023 Contenders Autograph Capsule, 3.5, 1, CS
Sticker | MOUZ (Holo) | Paris 2023, 15.2, 1, CS
Paris 2023 Mirage Souvenir Package, 50.6, 2, CS
Pirate Facemask, 10, 2, RUST
Mann Co. Supply Crate Key, 5, 10, TF2
```
Here's the list of games:
```txt
    "STEAM" - Steam Market (ingame cards, wallpapers)
    "DOTA2" - Dota 2 Market
    "CS" - CS2 Market
    "TF2" - TF2 Market
    "PUBG" - Pubg Market
    "RUST" - Rust 
```

## Running the Bot
1. Open a terminal or command prompt in the correct folder with the BuyOrderBot script.
2. Enter the following command to start the bot:

```python
python buy_order_bot.py
```

The bot will automatically log in to your Steam account and start placing Buy Orders for your items.

Follow the previous instructions and monitor the messages displayed in the terminal to ensure that your BuyOrderBot is working properly.

## Currencies

| Currency class | Description                 |
| ---            | ---                         |
| Currency.USD   | United States Dollar        |
| Currency.GBP   | United Kingdom Pound        |
| Currency.EURO  | European Union Euro         |
| Currency.CHF   | Swiss Francs                |
| Currency.RUB   | Russian Rouble              |
| Currency.PLN   | Polish Złoty                |
| Currency.BRL   | Brazilian Reals             |
| Currency.JPY   | Japanese Yen                |
| Currency.NOK   | Norwegian Krone             |
| Currency.IDR   | Indonesian Rupiah           |
| Currency.MYR   | Malaysian Ringgit           |
| Currency.PHP   | Philippine Peso             |
| Currency.SGD   | Singapore Dollar            |
| Currency.THB   | Thai Baht                   |
| Currency.VND   | Vietnamese Dong             |
| Currency.KRW   | South Korean Won            |
| Currency.TRY   | Turkish Lira                |
| Currency.UAH   | Ukrainian Hryvnia           |
| Currency.MXN   | Mexican Peso                |
| Currency.CAD   | Canadian Dollars            |
| Currency.AUD   | Australian Dollars          |
| Currency.NZD   | New Zealand Dollar          |
| Currency.CNY   | Chinese Renminbi (yuan)     |
| Currency.INR   | Indian Rupee                |
| Currency.CLP   | Chilean Peso                |
| Currency.PEN   | Peruvian Sol                |
| Currency.COP   | Colombian Peso              |
| Currency.ZAR   | South African Rand          |
| Currency.HKD   | Hong Kong Dollar            |
| Currency.TWD   | New Taiwan Dollar           |
| Currency.SAR   | Saudi Riyal                 |
| Currency.AED   | United Arab Emirates Dirham |
| Currency.SEK   | Swedish Krona               |
| Currency.ARS   | Argentine Peso              |
| Currency.ILS   | Israeli New Shekel          |
| Currency.BYN   | Belarusian Ruble            |
| Currency.KZT   | Kazakhstani Tenge           |
| Currency.KWD   | Kuwaiti Dinar               |
| Currency.QAR   | Qatari Riyal                |
| Currency.CRC   | Costa Rican Colón           |
| Currency.UYU   | Uruguayan Peso              |
| Currency.BGN   | Bulgarian Lev               |
| Currency.HRK   | Croatian Kuna               |
| Currency.CZK   | Czech Koruna                |
| Currency.DKK   | Danish Krone                |
| Currency.HUF   | Hungarian Forint            |
| Currency.RON   | Romanian Leu                |