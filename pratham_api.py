import requests
import matplotlib.pyplot as plt
from datetime import datetime

def get_etherscan_transactions(api_key, address, start_block=None, end_block=None):
    base_url = "https://api.etherscan.io/api"
    module = "account"
    action = "txlist"
    sort = "desc"

    params = {
        'apikey': api_key,
        'module': module,
        'action': action,
        'address': address,
        'sort': sort,
    }

    if start_block:
        params['startblock'] = start_block

    if end_block:
        params['endblock'] = end_block

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if data['status'] == '1':
            transactions = data['result']
            return transactions
        else:
            print(f"Error: {data['message']}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None


def plot_transactions(transactions):
    if transactions:
        time_values = [datetime.fromtimestamp(int(tx['timeStamp'])) for tx in transactions]
        ether_values = [float(tx['value']) / 1e18 for tx in transactions]
        gas_values = [float(tx['gasPrice']) / 1e18 for tx in transactions]

        plt.figure(figsize=(12, 10))

        # Plot 1: Time vs Ether Value
        plt.subplot(3, 1, 1)
        plt.plot(time_values, ether_values, marker='o', linestyle='-', color='b')
        plt.title('Account Time vs Ether(ETH) Value')
        plt.xlabel('Time')
        plt.ylabel('Ether(ETH) Value')

        # Plot 2: Time vs Gas Paid
        plt.subplot(3, 1, 2)
        plt.plot(time_values, gas_values, marker='o', linestyle='-', color='r')
        plt.title('Account Time vs Gas Paid (ETH)')
        plt.xlabel('Time')
        plt.ylabel('Gas Paid (ETH)')

        # Plot 3: Ether Value vs Gas Paid
        plt.subplot(3, 1, 3)
        plt.scatter(ether_values, gas_values, color='green')
        plt.title('Ether(ETH) Value vs Gas Paid (ETH)')
        plt.xlabel('Ether(ETH) Value')
        plt.ylabel('Gas Paid (ETH)')

        plt.tight_layout()
        plt.show()

        # Additional visualization: Ether Value Distribution
        plt.figure(figsize=(8, 6))
        plt.hist(ether_values, bins=20, color='blue', edgecolor='black')
        plt.title('Distribution of Ether(ETH) Transaction Values')
        plt.xlabel('Ether(ETH) Value')
        plt.ylabel('Frequency')
        plt.show()
    else:
        print("Error: Unable to fetch transactions.")


api_key = '1Z5ZIRYR112JYDBKV8T35VRAEFU8DF366I'
user_address = '0x95222290DD7278Aa3Ddd389Cc1E1d165CC4BAfe5'

transactions = get_etherscan_transactions(api_key, user_address)

if transactions:
    print(f"Total transactions for {user_address}: {len(transactions)}")
    plot_transactions(transactions)
else:
    print("Error: Unable to fetch transactions.")