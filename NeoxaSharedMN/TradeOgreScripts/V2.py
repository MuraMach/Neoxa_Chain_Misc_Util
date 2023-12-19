import requests

API_BASE_URL = 'https://tradeogre.com/api/v1'

def make_api_request(endpoint):
    response = requests.get(endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def get_markets():
    endpoint = f'{API_BASE_URL}/markets'
    return make_api_request(endpoint)

def get_order_book(market):
    endpoint = f'{API_BASE_URL}/orders/{market}'
    return make_api_request(endpoint)

def get_ticker(market):
    endpoint = f'{API_BASE_URL}/ticker/{market}'
    return make_api_request(endpoint)

def get_trade_history(market):
    endpoint = f'{API_BASE_URL}/history/{market}'
    return make_api_request(endpoint)

def display_market_info(markets):
    print("Available Markets:")
    for market in markets:
        print(market)

def display_data(data, data_type):
    if data:
        print(f"{data_type}:")
        print(data)
    else:
        print(f"Failed to retrieve the {data_type}.")

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
        display_market_info(markets)
    
    elif choice in ('2', '3', '4'):
        market = input("Enter the market (e.g., XMR-BTC): ")
        
        if choice == '2':
            display_data(get_order_book(market), "Order Book")
        elif choice == '3':
            display_data(get_ticker(market), "Ticker")
        elif choice == '4':
            display_data(get_trade_history(market), "Trade History")
    
    else:
        print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
##See note:
##99.9% Done , Prior version in this directory works as intended,  this is a
##clean-up , status will be complete once fully tested.
##Final will be named TradeOgrePubAPI.py -> For Neoxa Community.
