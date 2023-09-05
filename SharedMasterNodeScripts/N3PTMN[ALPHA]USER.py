##THIS IS NOT PRODUCTION READY , DO NOT USE IN NON TEST NET ENVIRONMENT##
##THIS IS IN BTC SCRIPT , FOR DASH RPC AND NEOXA RPC YOU NEED TO CHANGE PARAMETERS THIS IS DONE PURPOSELY SO YOU MUST DO THIS YOURSELF -- RPC NAMES NEED TO BE CHANGED ACCORDING TO CHAIN##
##YOU MAY ENCOUNTER ERRORS AND BUGS , PLEASE REPORT THEM IF YOU TRY THIS YOURSELF##

from bitcoin.core import CTransaction, CTxIn, CTxOut, CScript
from bitcoin.core.script import OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG

# Define User's Public Key and Collateral Amount
user_pubkey = 'User_Public_Key'
user_collateral = 10000000  # Adjust this to match the collateral amount you want to deposit

# Function to create the collateral deposit transaction
def create_collateral_deposit_tx(user_pubkey, user_collateral):
    tx = CTransaction()

    # Create the user's deposit script
    user_script = CScript([
        OP_DUP,
        OP_HASH160, bytes.fromhex(user_pubkey),
        OP_EQUALVERIFY,
        OP_CHECKSIG,
    ])

    # Create the user's output for collateral deposit
    user_output = CTxOut(user_collateral, user_script)
    tx.add_out(user_output)

    return tx

# Function to spend funds from the user's collateral output
def spend_user_collateral(inputs, recipient_pubkey, change_pubkey, user_collateral):
    tx = CTransaction()

    # Add inputs (UTXOs) to the transaction
    for txid, vout in inputs:
        tx.add_in(CTxIn(COutPoint(int(txid, 16), vout)))

    # Create the recipient output
    recipient_output = CTxOut(user_collateral - 10000, CScript([OP_DUP, OP_HASH160, bytes.fromhex(recipient_pubkey), OP_EQUALVERIFY, OP_CHECKSIG]))
    tx.add_out(recipient_output)

    # Create the change output
    change_output = CTxOut(10000, CScript([OP_DUP, OP_HASH160, bytes.fromhex(change_pubkey), OP_EQUALVERIFY, OP_CHECKSIG]))
    tx.add_out(change_output)

    return tx

if __name__ == "__main__":
    try:
        # Create the collateral deposit transaction
        deposit_tx = create_collateral_deposit_tx(user_pubkey, user_collateral)

        # Serialize and print the collateral deposit transaction
        serialized_deposit_tx = deposit_tx.serialize().hex()
        print("Collateral deposit transaction created successfully:")
        print(serialized_deposit_tx)

        # In a real scenario, this part would be done by the user
        recipient_pubkey = 'Recipient_Public_Key'  # Replace with the recipient's public key
        change_pubkey = 'Change_Public_Key'  # Replace with the change address public key

        # Create a transaction to spend user's collateral
        spend_tx = spend_user_collateral([(serialized_deposit_tx, 0)], recipient_pubkey, change_pubkey, user_collateral)

        # Serialize and print the spend transaction
        serialized_spend_tx = spend_tx.serialize().hex()
        print("\nSpend transaction created successfully:")
        print(serialized_spend_tx)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
