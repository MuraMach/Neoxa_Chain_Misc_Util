from dashd.wallet import Wallet
from dashd.transaction import Transaction, TxInput, TxOutput
from dashd.script import Script

# Function to create an envelope with SVG content
def create_svg_envelope(svg_content):
    envelope_script = Script()
    envelope_script << 'OP_FALSE' << 'OP_IF' << 'OP_PUSH "svg"' << 'OP_PUSH 1' << 'OP_PUSH "image/svg+xml"' << 'OP_PUSH 0' << f'OP_PUSH "{svg_content}"' << 'OP_ENDIF'
    return envelope_script

# Function to create a two-phase commit transaction
def create_commit_transaction(wallet, envelope_script):
    commit_tx = Transaction()
    commit_tx.add_input(wallet.get_utxos()[0])
    commit_tx.add_output(value=0, script=envelope_script)
    return commit_tx

# Function to create the reveal transaction
def create_reveal_transaction(wallet, commit_tx):
    # Retrieve information from the commit transaction
    commit_output = commit_tx.outputs[0]
    commit_script = commit_output.script

    # Create a transaction to spend from the commit transaction
    reveal_tx = Transaction()
    reveal_tx.add_input(commit_tx.hash, 0, commit_script)
    reveal_tx.add_output(value=0, script=Script())  # Dummy output, change as needed

    # Sign the reveal transaction
    reveal_tx.sign(wallet.get_private_key())

    return reveal_tx
