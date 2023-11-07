import requests
import json

# Constants for RPC configuration
RPC_ENDPOINT = "http://127.0.0.1:9998"
RPC_USERNAME = "your_rpc_username"
RPC_PASSWORD = "your_rpc_password"

def send_rpc_request(method, params=None):
    """Send an RPC request to the blockchain."""
    payload = {
        "method": method,
        "params": params or [],
        "jsonrpc": "2.0",
        "id": 1,
    }

    response = requests.post(RPC_ENDPOINT, json=payload, auth=(RPC_USERNAME, RPC_PASSWORD))
    result = response.json()

    if "error" in result:
        raise Exception(f"RPC Error: {result['error']}")

    return result["result"]

def calculate_and_send_payments(recipient_data, total_rewards, total_stake):
    """Calculate and send payments to recipients based on their stakes."""
    addresses_and_percentages = [(address, (stake / total_stake) * 100) for address, stake in recipient_data]

    print("\nAddresses and Percentages Owned for Payments:")
    for address, percentage in addresses_and_percentages:
        print(f"Address: {address}, Percentage: {percentage:.2f}%")

    total_amount_to_send = total_rewards

    print(f"\nTotal amount to send: {total_amount_to_send:.8f} coins")

    send_payouts = input("\nSEND PAYMENTS? (yes/no): ").lower()

    if send_payouts == "yes":
        for address, percentage in addresses_and_percentages:
            amount_to_send = (percentage / 100) * total_amount_to_send
            formatted_amount = "{:.8f}".format(amount_to_send)
            try:
                txid = send_rpc_request("sendtoaddress", [address, formatted_amount])
                print(f"Payment of {formatted_amount} coins sent to {address}. Transaction ID: {txid}")
            except Exception as e:
                print(f"Sending payment to {address}: {e}")

if __name__ == '__main__':
    # Example usage to send payments
    recipient_data = [("address1", 500000), ("address2", 200000), ("address3", 300000)]
    total_rewards = 0001  # Total amount to distribute
    total_stake = sum(stake for _, stake in recipient_data)
    calculate_and_send_payments(recipient_data, total_rewards, total_stake)
