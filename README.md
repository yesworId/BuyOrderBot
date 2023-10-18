# BuyOrderBot
This is Bot designed to automate the process of placing buy orders for Steam Market items and make it much faster.\
I was using precious library called `steampy` for this. The author made such a good job. Big thanks to you `bukson`!\
If someone have any idea how to improve this program -> feel free to share it with me.

How does it work?
============
* First of all, bot log into your Steam account using provided credentials. Then it gets your account balance and calculates BuyOrder limit to compare the sum of the order ​​to it. BuyOrder limit is ten times your balance.
* Next step is to get total cost of all orders, so bot gets all of your BuyOrder listing, which still active on account for this. The program subtracts the value of the total cost from the BuyOrder limit and gets the current value of BuyOrder limit.
* After all of this, bot is ready to place buy orders. It goes through each item in your items.csv file and tries to place buy order.
* Program finishes after all items successfully got active buy order.

Setup
============

First of all create config.json file

**Your config.json file should look like this for the proper work**

```json
{
  "api_key": "YOUR_API_KEY",
  "username": "YOUR_USERNAME",
  "password": "YOUR_PASSWORD",
  "currency": "YOUR_CURRENCY"
}
```
* [Obtaining API key](https://steamcommunity.com/dev/apikey)
* [Choose your currency](https://github.com/YESW0RLD/BuyOrderBot/blob/master/README.md#currencies)

**Example of config.json:**
```json
{
  "api_key": "46302079E204013FGA3E2CA89825469A",
  "username": "username1",
  "password": "password1",
  "currency": "UAH"
}
```

Then, you need to obtain shared_secret from MaFile and save it in **steam_guard.json** file
* [Obtaining MaFile from Steam Desktop Authenticator](https://github.com/SteamTimeIdler/stidler/wiki/Getting-your-%27shared_secret%27-code-for-use-with-Auto-Restarter-on-Mobile-Authentication#getting-shared-secret-from-steam-desktop-authenticator-windows)

**Now your steam_guard.json file should look like this**

```json
{
    "steamid": "YOUR_STEAM_ID",
    "shared_secret": "YOUR_SHARED_SECRET",
    "identity_secret": "YOUR_IDENTITY_SECRET"
  }
```
Usage
============
You already decided which items you want to buy.

Now you need to create items.csv file where you write down all the item names with the prices and item amount you want to buy.

**Warning!**
First you must write the name of the item, then price you want to buy it for, and the amount of those items. You can set the prices at the same way as you do it on Steam Market

**Example:**
``` csv
Name, Price, Amount
Snakebite Case, 1.5, 2
Operation Bravo Case, 10.6, 1
AK-47 | Asiimov (Field-Tested), 5.7, 1
Paris 2023 Contenders Autograph Capsule, 3.5, 1
Sticker | MOUZ (Holo) | Paris 2023, 15.2, 1
Paris 2023 Mirage Souvenir Package, 50.6, 2
Sticker | Apeks (Holo) | Paris 2023, 5.09, 1
```

Running the Bot
============
1. Open a terminal or command prompt in the folder with the BuyOrderBot script.
2. Enter the following command to start the bot:

```python
python buy_order_bot.py
```

1. The bot will automatically log in to your Steam account and start placing Buy Orders for your items.

Follow the previous instructions and monitor the messages displayed in the terminal to ensure that your BuyOrderBot is working properly.

Currencies
----------

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