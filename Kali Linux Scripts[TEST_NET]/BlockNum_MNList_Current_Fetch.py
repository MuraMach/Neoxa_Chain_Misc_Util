import requests

testnet_explorer_url = 'http://51.178.41.227:3001'

def make_api_call(endpoint):
    response = requests.get(f"{testnet_explorer_url}/{endpoint}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Return data from coind

def get_difficulty():
    return make_api_call("api/getdifficulty")

def get_connection_count():
    return make_api_call("api/getconnectioncount")

def get_block_count():
    return make_api_call("api/getblockcount")

def get_block_hash(index):
    endpoint = f"api/getblockhash?index={index}"
    return make_api_call(endpoint)

def get_block(block_hash):
    endpoint = f"api/getblock?hash={block_hash}"
    return make_api_call(endpoint)

def get_raw_transaction(txid, decrypt):
    endpoint = f"api/getrawtransaction?txid={txid}&decrypt={decrypt}"
    return make_api_call(endpoint)

def get_network_hashrate():
    return make_api_call("api/getnetworkhashps")

def get_vote_list():
    return make_api_call("api/getvotelist")

def get_masternode_count():
    return make_api_call("api/getmasternodecount")

# Extended API

def get_money_supply():
    return make_api_call("ext/getmoneysupply")

def get_distribution():
    return make_api_call("ext/getdistribution")

def get_address_info(address):
    endpoint = f"ext/getaddress/{address}"
    return make_api_call(endpoint)

def get_address_transactions(address, start, length):
    endpoint = f"ext/getaddresstxs/{address}/{start}/{length}"
    return make_api_call(endpoint)

def get_transaction(tx_hash):
    endpoint = f"ext/gettx/{tx_hash}"
    return make_api_call(endpoint)

def get_balance(address):
    endpoint = f"ext/getbalance/{address}"
    return make_api_call(endpoint)

def get_last_transactions(min_coins, start, length):
    endpoint = f"ext/getlasttxs/{min_coins}/{start}/{length}"
    return make_api_call(endpoint)

def get_current_price():
    return make_api_call("ext/getcurrentprice")

def get_network_peers():
    return make_api_call("ext/getnetworkpeers")

def get_basic_stats():
    return make_api_call("ext/getbasicstats")

def get_summary():
    return make_api_call("ext/getsummary")

def get_masternode_list():
    return make_api_call("ext/getmasternodelist")

def get_masternode_rewards(address, since):
    endpoint = f"ext/getmasternoderewards/{address}/{since}"
    return make_api_call(endpoint)

def get_masternode_rewards_total(address, since):
    endpoint = f"ext/getmasternoderewardstotal/{address}/{since}"
    return make_api_call(endpoint)

# Function to display the menu options
def display_menu():
    print("Menu:")
    print("1. Get Current Block Count")
    print("2. Get Masternode Information")
    print("3. Get Basic Statistics")
    print("4. Get Difficulty")
    print("5. Get Money Supply")
    print("6. Get Network Hashrate")
    print("7. Get Address Information")
    print("8. Exit")

# Retrieve current block count
def get_current_block_count():
    block_count_data = get_block_count()
    if block_count_data is not None:
        if isinstance(block_count_data, int):
            block_count = block_count_data
        else:
            block_count = block_count_data['result']
        print(f"Current Block Count: {block_count}")
    else:
        print("Failed to retrieve block count.")

# Retrieve masternode information
def get_masternode_info():
    masternodes_data = get_masternode_list()
    if masternodes_data is not None:
        for masternode in masternodes_data:
            print(f"- IP: {masternode['addr']}, Status: {masternode['status']}")
    else:
        print("Failed to retrieve masternode information.")

# Retrieve basic statistics
def get_basic_statistics():
    basic_stats_data = get_basic_stats()
    if basic_stats_data is not None:
        block_count = basic_stats_data['block_count']
        money_supply = basic_stats_data['money_supply']
        last_price_btc = basic_stats_data['last_price_btc']
        last_price_usd = basic_stats_data['last_price_usd']
        masternode_count = basic_stats_data['masternode_count']

        print(f"Block Count: {block_count}")
        print(f"Money Supply: {money_supply}")
        print(f"Last Price (BTC): {last_price_btc}")
        print(f"Last Price (USD): {last_price_usd}")
        print(f"Masternode Count: {masternode_count}")
    else:
        print("Failed to retrieve basic statistics.")

# Retrieve difficulty
def get_difficulty_data():
    difficulty_data = get_difficulty()
    if difficulty_data is not None:
        print(difficulty_data)
    else:
        print("Failed to retrieve difficulty.")

# Retrieve money supply
def get_money_supply_data():
    money_supply_data = get_money_supply()
    if money_supply_data is not None:
        print(f"Money Supply: {money_supply_data}")
    else:
        print("Failed to retrieve money supply.")

# Retrieve network hashrate
def get_network_hashrate_data():
    network_hashrate_data = get_network_hashrate()
    if network_hashrate_data is not None:
        print(f"Network Hashrate: {network_hashrate_data}")
    else:
        print("Failed to retrieve network hashrate.")

# Retrieve address information
def get_address_info_data():
    address = input("Enter the address: ")
    address_info_data = get_address_info(address)
    if address_info_data is not None:
        print(f"Address Information: {address_info_data}")
    else:
        print("Failed to retrieve address information.")

# Main program loop
while True:
    display_menu()
    choice = input("Enter your choice (1-8): ")

    if choice == '1':
        get_current_block_count()

    elif choice == '2':
        get_masternode_info()

    elif choice == '3':
        get_basic_statistics()

    elif choice == '4':
        get_difficulty_data()

    elif choice == '5':
        get_money_supply_data()

    elif choice == '6':
        get_network_hashrate_data()

    elif choice == '7':
        get_address_info_data()

    elif choice == '8':
        print("Exiting...")
        break

    else:
        print("Invalid choice. Please try again.\n")
