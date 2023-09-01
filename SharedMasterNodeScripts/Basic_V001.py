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

def get_recipient_data():
    """Get recipient addresses and their stakes."""
    total_rewards = float(input("Enter reward amount to distribute: "))
    num_addresses = int(input("Enter the number of recipient addresses: "))

    recipient_data = []
    total_stake = 0

    for i in range(num_addresses):
        address = input(f"Enter recipient address {i + 1}: ")
        stake = float(input(f"Enter coins staked out of 1M(1,000,000) for {address}: "))
        total_stake += stake
        recipient_data.append((address, stake))

    return recipient_data, total_rewards, total_stake

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

# Function for Timelock (not implemented yet)
def timelock():
    print("Timelock function is not implemented yet.")

# Function for N3PTMN_Setup_ADDR (not implemented yet)
def n3ptmn_setup_addr():
    print("N3PTMN_Setup_ADDR function is not implemented yet.")

# Function for N3PTMN_Check_SECURE (not implemented yet)
def n3ptmn_check_secure():
    print("N3PTMN_Check_SECURE function is not implemented yet.")

# Function for N3PTMN_User_COLATS (not implemented yet)
def n3ptmn_user_colats():
    print("N3PTMN_User_COLATS function is not implemented yet.")

# Function for N3PTMN_testsnotdone (not implemented yet)
def n3ptmn_testsnotdone():
    print("N3PTMN_testsnotdone function is not implemented yet.")

def main():
    """Main function to execute the menu system."""
    while True:
        print("\nMENU:")
        print("1. Send Payments")
        print("2. Timelock (Not Implemented)")
        print("3. N3PTMN_Setup_ADDR (Not Implemented)")
        print("4. N3PTMN_Check_SECURE (Not Implemented)")
        print("5. N3PTMN_User_COLATS (Not Implemented)")
        print("6. N3PTMN_testsnotdone (Not Implemented)")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            recipient_data, total_rewards, total_stake = get_recipient_data()
            calculate_and_send_payments(recipient_data, total_rewards, total_stake)
        elif choice == "2":
            timelock()
        elif choice == "3":
            n3ptmn_setup_addr()
        elif choice == "4":
            n3ptmn_check_secure()
        elif choice == "5":
            n3ptmn_user_colats()
        elif choice == "6":
            n3ptmn_testsnotdone()
        elif choice == "7":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
