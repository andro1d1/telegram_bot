import requests
from utils.cred_helper import get_value

def get_rate(base_curr: str, need_curr: str, count):
    """
    Returns a sum in the right currency
    """
    api_key = get_value('EXCHANGE_API')
    url = f"https://api.apilayer.com/exchangerates_data/convert?to={need_curr}&from={base_curr}&amount={count}"
    headers = {
        "apikey": api_key
    }
    payload = {}

    response = requests.request("GET", url, headers=headers, data = payload)
    return response.json().get("result")
