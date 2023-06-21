import requests

testnet_explorer_url = 'http://51.178.41.227:3001'

def get_block_count():
    response = requests.get(f"{testnet_explorer_url}/api/getblockcount")
    if response.status_code == 200:
        block_count = response.json()
        return block_count
    else:
        return None

def get_masternodes():
    response = requests.get(f"{testnet_explorer_url}/ext/getmasternodelist")
    if response.status_code == 200:
        masternodes = response.json()
        return masternodes
    else:
        return None

# Retrieve current block count
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
masternodes_data = get_masternodes()
if masternodes_data is not None:
    for masternode in masternodes_data:
        print(f"- IP: {masternode['addr']}, Status: {masternode['status']}")
else:
    print("Failed to retrieve masternode information.")
