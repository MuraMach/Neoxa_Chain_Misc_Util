# MIT License
# © MuraMach(Leos)
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import requests

API_BASE_URL = 'https://tradeogre.com/api/v1'

def get_markets():
    endpoint = f'{API_BASE_URL}/markets'
    response = requests.get(endpoint)
    if response.status_code == 200:
        markets = response.json()
        return markets
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def get_order_book(market):
    endpoint = f'{API_BASE_URL}/orders/{market}'
    response = requests.get(endpoint)
    if response.status_code == 200:
        order_book = response.json()
        return order_book
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def get_ticker(market):
    endpoint = f'{API_BASE_URL}/ticker/{market}'
    response = requests.get(endpoint)
    if response.status_code == 200:
        ticker = response.json()
        return ticker
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def get_trade_history(market):
    endpoint = f'{API_BASE_URL}/history/{market}'
    response = requests.get(endpoint)
    if response.status_code == 200:
        trade_history = response.json()
        return trade_history
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def main():
    print("Welcome to the TradeOgre Public API Client!")
    print("Choose an option:")
    print("1. Get Markets")
    print("2. Get Order Book")
    print("3. Get Ticker")
    print("4. Get Trade History")
    
    choice = input("Enter your choice (1-4): ")
    
    if choice == '1':
        markets = get_markets()
        if markets:
            print("Markets:")
            for market in markets:
                print(market)
    
    elif choice == '2':
        market = input("Enter the market (e.g., XMR-BTC): ")
        order_book = get_order_book(market)
        if order_book:
            print("Order Book:")
            print(order_book)
    
    elif choice == '3':
        market = input("Enter the market (e.g., XMR-BTC): ")
        ticker = get_ticker(market)
        if ticker:
            print("Ticker:")
            print(ticker)
    
    elif choice == '4':
        market = input("Enter the market (e.g., XMR-BTC): ")
        trade_history = get_trade_history(market)
        if trade_history:
            print("Trade History:")
            print(trade_history)
    
    else:
        print("Invalid choice. Please try again.")
        return

if __name__ == '__main__':
    main()
