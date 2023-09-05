##THIS IS NOT PRODUCTION READY , DO NOT USE IN NON TEST NET ENVIRONMENT##
##THIS IS IN BTC SCRIPT , FOR DASH RPC AND NEOXA RPC YOU NEED TO CHANGE PARAMETERS THIS IS DONE PURPOSELY SO YOU MUST DO THIS YOURSELF -- RPC NAMES NEED TO BE CHANGED ACCORDING TO CHAIN##
##YOU MAY ENCOUNTER ERRORS AND BUGS , PLEASE REPORT THEM IF YOU TRY THIS YOURSELF##

from bitcoin.core import CTransaction, COutPoint, CTxIn, CTxOut
from bitcoin.core.script import CScript, OP_IF, OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG, OP_ELSE, OP_CHECKLOCKTIMEVERIFY, OP_DROP, OP_ENDIF
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH

# Define Operator's Public Key
operator_pubkey = 'Operator_Public_Key'

# Define Lock Time in Blocks (e.g., 2 weeks)
lock_time_blocks = 2016  # Adjust this according to your desired lock duration

# Define Participants' Public Keys
participants_pubkeys = [
    'Participant1_Public_Key',
    'Participant2_Public_Key',
    # Add more participant public keys as needed
]

# Create a list of participants and their allocated collateral
participants = [
    {'pubkey': 'Participant1_Public_Key', 'collateral': 10000000},  # Adjust collateral amounts as needed
    {'pubkey': 'Participant2_Public_Key', 'collateral': 10000000},
]

# Function to create the Masternode activation transaction
def create_masternode_tx(inputs, operator_pubkey, participants, lock_time_blocks):
    tx = CTransaction()

    # Add inputs (UTXOs) to the transaction
    for txid, vout in inputs:
        tx.add_in(CTxIn(COutPoint(int(txid, 16), vout)))

    # Create the operator's script
    operator_script = CScript([
        OP_IF,
        OP_DUP,
        OP_HASH160, bytes.fromhex(operator_pubkey),
        OP_EQUALVERIFY,
        OP_CHECKSIG,
        OP_ELSE,
        lock_time_blocks,
        OP_CHECKLOCKTIMEVERIFY,
        OP_DROP,
    ])

    # Add participants' public keys to the script
    for participant in participants:
        operator_script.extend([OP_DUP, OP_HASH160, bytes.fromhex(participant['pubkey']), OP_EQUALVERIFY, OP_CHECKSIG])

    operator_script.append(OP_ENDIF)

    # Create the operator's output
    operator_output = CTxOut(participants[0]['collateral'], operator_script)
    tx.add_out(operator_output)

    return tx

# Function to spend funds from the operator's output
def spend_operator_funds(inputs, recipient_pubkey, change_pubkey, operator_output_value):
    tx = CTransaction()

    # Add inputs (UTXOs) to the transaction
    for txid, vout in inputs:
        tx.add_in(CTxIn(COutPoint(int(txid, 16), vout)))

    # Create the recipient output
    recipient_output = CTxOut(operator_output_value - 10000, CScript([OP_DUP, OP_HASH160, bytes.fromhex(recipient_pubkey), OP_EQUALVERIFY, OP_CHECKSIG]))
    tx.add_out(recipient_output)

    # Create the change output
    change_output = CTxOut(10000, CScript([OP_DUP, OP_HASH160, bytes.fromhex(change_pubkey), OP_EQUALVERIFY, OP_CHECKSIG]))
    tx.add_out(change_output)

    return tx

if __name__ == "__main__":
    # Replace these with your actual input UTXOs and collateral value
    input_utxos = [
        ('input_txid_1', 0),
        ('input_txid_2', 1),
        # Add more input UTXOs as needed
    ]

    try:
        # Create the Masternode activation transaction
        masternode_tx = create_masternode_tx(input_utxos, operator_pubkey, participants, lock_time_blocks)

        # Serialize and print the Masternode activation transaction
        serialized_masternode_tx = masternode_tx.serialize().hex()
        print("Masternode activation transaction created successfully:")
        print(serialized_masternode_tx)

        # In a real scenario, this part would be done by participants
        recipient_pubkey = 'Recipient_Public_Key'  # Replace with the recipient's public key
        change_pubkey = 'Change_Public_Key'  # Replace with the change address public key

        # Create a transaction to spend operator's funds
        spend_tx = spend_operator_funds([(serialized_masternode_tx, 0)], recipient_pubkey, change_pubkey, participants[0]['collateral'])

        # Serialize and print the spend transaction
        serialized_spend_tx = spend_tx.serialize().hex()
        print("\nSpend transaction created successfully:")
        print(serialized_spend_tx)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
