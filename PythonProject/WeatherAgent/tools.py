import requests
from pathlib import Path

def get_gold_rate():
    try:
        response = requests.get('https://api.metalpriceapi.com/v1/latest?api_key=c9af6f2f2c7b31702d55f6e641ece0ff&base=INR&currencies=XAU')  # Use a real endpoint
        if response.status_code == 200:
            data = response.json()
            print(round((data['rates']['INRXAU']/31.1035),2))
            # return data['price']  # Adjust based on actual response structure
        else:
            return response.status_code
    except Exception as e:
        return str(e)

print(type(get_gold_rate()))

print(Path("tools.py").resolve())
