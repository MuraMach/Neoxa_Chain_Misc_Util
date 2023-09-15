from bitcoin.core import CTransaction, COutPoint, CTxIn, CTxOut, CScript, OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG, OP_ELSE, OP_CHECKLOCKTIMEVERIFY, OP_DROP, OP_ENDIF
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH
from bitcoin.wallet import P2SHBitcoinAddress
import hashlib

# Define Operator and Participants' Public Keys
operator_pubkey = 'Operator_Public_Key'
participant1_pubkey = 'Participant1_Public_Key'
participant2_pubkey = 'Participant2_Public_Key'
# Add more participant public keys as needed

# Define Lock Time in Blocks (e.g., 2 weeks)
lock_time_blocks = 2016  # Adjust this according to your desired lock duration

# Define the number of required signatures (participants)
required_signatures = 2  # Adjust this based on your multisig requirements

# Function to create a multisig address
def create_multisig_address(pubkeys, required_signatures):
    redeem_script = CScript([required_signatures] + pubkeys + [len(pubkeys), OP_CHECKMULTISIG])
    redeem_script_hex = redeem_script.hex()
    redeem_script_hash = hashlib.sha256(bytes.fromhex(redeem_script_hex)).digest()
    multisig_address = P2SHBitcoinAddress.from_bytes(redeem_script_hash)
    return multisig_address, redeem_script

# Create the multisig address and redeem script
multisig_pubkeys = [bytes.fromhex(operator_pubkey), bytes.fromhex(participant1_pubkey), bytes.fromhex(participant2_pubkey)]
multisig_address, redeem_script = create_multisig_address(multisig_pubkeys, required_signatures)

# Print the multisig address for participants to send funds to
print(f"Multisig Address: {multisig_address}")

# Function to create the Masternode activation transaction
def create_masternode_tx(inputs, multisig_address, lock_time_blocks):
    tx = CTransaction()

    # Add inputs (UTXOs) to the transaction
    for txid, vout in inputs:
        tx.add_in(CTxIn(COutPoint(int(txid, 16), vout)))

    # Create the operator's output with the multisig script
    operator_output = CTxOut(participants[0]['collateral'], CScript([OP_HASH160, multisig_address.to_hash160(), OP_EQUAL]))
    tx.add_out(operator_output)

    return tx

# Function to spend funds from the operator's output
def spend_operator_funds(inputs, multisig_address, change_pubkey, operator_output_value):
    tx = CTransaction()

    # Add inputs (UTXOs) to the transaction
    for txid, vout in inputs:
        tx.add_in(CTxIn(COutPoint(int(txid, 16), vout)))

    # Create the recipient output using the multisig address
    recipient_output = CTxOut(operator_output_value - 10000, CScript([OP_HASH160, multisig_address.to_hash160(), OP_EQUAL]))
    tx.add_out(recipient_output)

    # Create the change output
    change_output = CTxOut(10000, CScript([OP_DUP, OP_HASH160, bytes.fromhex(change_pubkey), OP_EQUALVERIFY, OP_CHECKSIG]))
    tx.add_out(change_output)

    return tx

# Function to create a redemption transaction for participants
def create_redemption_tx(input_txid, input_vout, participant_pubkey, collateral_amount, recipient_address):
    tx = CTransaction()

    # Add the collateral input to the transaction
    tx.add_in(CTxIn(COutPoint(int(input_txid, 16), input_vout)))

    # Create the output paying the participant's collateral to their recipient address
    participant_output = CTxOut(collateral_amount, CScript([OP_HASH160, bytes.fromhex(participant_pubkey), OP_EQUAL]))
    tx.add_out(participant_output)

    return tx

# Function to display the menu and get user's choice
def menu():
    print("\nChoose an option:")
    print("1. Create Masternode (MN)")
    print("2. Spend Operator Funds (OP)")
    print("3. Create Redemption Transaction (REDEEM)")
    print("4. Quit (Q)")
    choice = input("Enter the option number: ").strip().lower()
    return choice

if __name__ == "__main__":
    while True:
        user_choice = menu()
        
        if user_choice == '1':
            # Creating a Masternode (MN)
            # Replace these with your actual input UTXOs and collateral values
            input_utxos = [
                ('input_txid_1', 0),
                ('input_txid_2', 1),
                # Add more input UTXOs as needed
            ]
            
            try:
                masternode_tx = create_masternode_tx(input_utxos, multisig_address, lock_time_blocks)
                serialized_masternode_tx = masternode_tx.serialize().hex()
                print("Masternode activation transaction created successfully:")
                print(serialized_masternode_tx)
            except Exception as e:
                print(f"An error occurred: {str(e)}")
        
        elif user_choice == '2':
            # Spending Operator Funds (OP)
            # In a real scenario, this part would be done by the operator
            change_pubkey = 'Change_Public_Key'  # Replace with the change address public key
            
            try:
                spend_tx = spend_operator_funds([(serialized_masternode_tx, 0)], multisig_address, change_pubkey, participants[0]['collateral'])
                serialized_spend_tx = spend_tx.serialize().hex()
                print("Spend transaction created successfully:")
                print(serialized_spend_tx)
            except Exception as e:
                print(f"An error occurred: {str(e)}")
        
        elif user_choice == '3':
            # Creating a Redemption Transaction (REDEEM)
            # For each participant, create a redemption transaction
            # Replace 'Recipient_Address' with the actual recipient address for each participant
            for participant in participants:
                try:
                    redemption_tx = create_redemption_tx(serialized_masternode_tx, 0, participant['pubkey'], participant['collateral'], 'Recipient_Address')
                    serialized_redemption_tx = redemption_tx.serialize().hex()
                    print(f"Redemption transaction for participant {participant['pubkey']} created successfully:")
                    print(serialized_redemption_tx)
                except Exception as e:
                    print(f"An error occurred for participant {participant['pubkey']}: {str(e)}")
        
        elif user_choice == '4' or user_choice.startswith('q'):
            break
        else:
            print("Invalid choice. Please select a valid option.")
