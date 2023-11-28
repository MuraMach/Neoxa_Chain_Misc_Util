import requests
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Neoxa RPC Configuration
RPC_USER = 'your_rpc_username'
RPC_PASSWORD = 'your_rpc_password'
RPC_URL = 'http://127.0.0.1:15419/'

# Function to make an RPC call to the Neoxa node
def rpc_call(method, params=None):
    payload = {
        'method': method,
        'jsonrpc': '2.0',
        'id': 1,
    }

    if params is not None:
        payload['params'] = params

    response = requests.post(RPC_URL, json=payload, auth=(RPC_USER, RPC_PASSWORD))

    if response.status_code != 200:
        raise Exception(f"RPC call failed with status code {response.status_code}: {response.text}")

    result = response.json().get('result')
    if result is None and 'error' in response.json():
        raise Exception(f"RPC call failed: {response.json()['error']['message']}")

    return result

# Function to get a list of available assets
def get_assets():
    return rpc_call('listassets', {'verbose': True})

# Function to get account balance
def get_balance(address):
    return rpc_call('getbalance', {'address': address})

# Function to transfer assets
def transfer_assets(sender_address, recipient_address, asset_name, amount):
    params = {
        'from': sender_address,
        'to': recipient_address,
        'asset': asset_name,
        'qty': amount,
    }
    return rpc_call('transfer', params)

# Route to display the main page with asset information
@app.route('/')
def index():
    assets = get_assets()
    return render_template('index.html', assets=assets)

# Route to handle asset transfers
@app.route('/transfer', methods=['POST'])
def transfer_assets_page():
    sender_address = request.form.get('sender_address')
    recipient_address = request.form.get('recipient_address')
    asset_name = request.form.get('asset_name')
    amount = request.form.get('amount')

    try:
        # Transfer assets
        transfer_assets(sender_address, recipient_address, asset_name, amount)

        flash('Asset transferred successfully!', 'success')
        return redirect(url_for('index'))

    except Exception as e:
        flash(f'Error transferring assets: {str(e)}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
