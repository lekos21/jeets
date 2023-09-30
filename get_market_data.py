import requests
import json
from config import etherscan_api


def get_market_info():
    # Define the base URL and parameters
    url = "https://api.etherscan.io/api"
    parameters = {
        'module': 'stats',
        'action': 'ethprice',
        'apikey': etherscan_api
    }
    # Make the GET request
    response = requests.get(url, params=parameters)

    # Ensure the response is successful
    response.raise_for_status()

    # Parse the JSON response
    data = response.json()

    # Check if the result is successful
    if data['status'] == '1':

        with open('games_data/eth_prices.json', 'r') as f:
            prices = json.load(f)

        if prices:
            prices["previous_price"] = prices["current_price"]
            prices["current_price"] = data['result']['ethusd']
            prices["variation"] = (prices["current_price"] / prices["previous_price"]) - 1



# execute the function
get_market_info()
