import os
from dotenv import load_dotenv
from binance.client import Client

load_dotenv()


def get_futures_client():
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        raise ValueError("BINANCE_API_KEY and BINANCE_API_SECRET are missing.")

    client = Client(api_key, api_secret)

    # Use Binance Futures Testnet
    client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

    return client