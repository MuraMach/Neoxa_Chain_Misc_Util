from dash import DashCoreRPC, CTransaction, CTxIn, CTxOut, CScript, OP_HASH160, hex_str_to_bytes, OP_CHECKSIG, OP_DROP, OP_IF, OP_ELSE, OP_ENDIF
import hashlib

# Replace with your Dash RPC connection details
rpc_connection = DashCoreRPC('http://username:password@localhost:port')

# Define the operator's public key
operator_pubkey = 'Operator_Public_Key'

# Define the number of required signatures (participants)
required_signatures = 2  # Adjust this based on your multisig requirements

# Dictionary to store individual participant collateral amounts
participant_collateral_amounts = {}

# Function to create a multisig address
def create_multisig_address(pubkeys, required_signatures):
    multisig_address = rpc_connection.addmultisigaddress(required_signatures, pubkeys)
    return multisig_address

# Function to create a transaction with multiple outputs
def create_transaction(inputs, outputs):
    tx = CTransaction()
    for txid, vout in inputs:
        tx.add_in(CTxIn(outpoint={'hash': txid, 'n': vout}))

    for address, amount in outputs.items():
        tx.add_out(CTxOut(nValue=int(amount * 1e8), scriptPubKey=CScript([OP_HASH160, hex_str_to_bytes(address), OP_EQUAL])))

    return tx

# Function to broadcast a transaction
def broadcast_transaction(tx):
    try:
        rpc_connection.sendrawtransaction(tx.serialize().hex())
        return True
    except Exception as e:
        print(f"Transaction broadcast failed: {str(e)}")
        return False

# Function to create a redemption transaction for a participant
def create_redemption_tx(participant_pubkey, collateral_amount, recipient_address):
    participant_address = rpc_connection.getaddressesbyaccount(participant_pubkey)[0]

    # Verify that the participant's collateral transaction is confirmed
    participant_utxos = rpc_connection.listunspent(0, 0, [participant_address])
    if not participant_utxos:
        print("Participant's collateral transaction is not confirmed yet.")
        return None

    tx = create_transaction([(participant_utxos[0]['txid'], participant_utxos[0]['vout'])],
                            {recipient_address: collateral_amount})
    return tx

# Function to combine participants' collateral into one address
def combine_participants_collateral(participants, multisig_address):
    total_collateral = 0
    for participant_pubkey, collateral_amount in participants.items():
        total_collateral += collateral_amount
        tx = create_redemption_tx(participant_pubkey, collateral_amount, multisig_address)
        if not tx:
            print(f"Failed to create redemption transaction for participant {participant_pubkey}")
            return
        if not broadcast_transaction(tx):
            print(f"Failed to broadcast redemption transaction for participant {participant_pubkey}")
            return
    print(f"Combined {total_collateral} collateral from participants into multisig address {multisig_address}")

# Main menu
def main_menu():
    print("\nChoose an option:")
    print("1. Create Redemption Transaction (Participant)")
    print("2. Combine Participants' Collateral (Operator)")
    print("3. Quit (Q)")

def main():
    multisig_address = create_multisig_address([operator_pubkey], required_signatures)

    while True:
        main_menu()
        choice = input("Enter the option number: ").strip().lower()

        if choice == '1':
            # Create Redemption Transaction (Participant)
            participant_pubkey = input("Enter your public key: ")
            collateral_amount = float(input("Enter your collateral amount (in DASH): "))
            recipient_address = input("Enter your Dash address for redemption: ")

            tx = create_redemption_tx(participant_pubkey, collateral_amount, recipient_address)
            if tx:
                if broadcast_transaction(tx):
                    print("Redemption transaction broadcasted successfully.")
                else:
                    print("Failed to broadcast the redemption transaction.")
            else:
                print("Failed to create the redemption transaction.")

        elif choice == '2':
            # Combine Participants' Collateral (Operator)
            participant_pubkeys = [input(f"Enter participant {i+1}'s public key: ") for i in range(required_signatures - 1)]
            collateral_amounts = [float(input(f"Enter collateral amount for participant {i+1} (in DASH): ")) for i in range(required_signatures - 1)]

            participants = dict(zip(participant_pubkeys, collateral_amounts))
            combine_participants_collateral(participants, multisig_address)

        elif choice == '3' or choice.startswith('q'):
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
