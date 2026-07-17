"""
Order placement functions.
"""

import logging
from binance.exceptions import BinanceAPIException, BinanceRequestException
from bot.client import get_futures_client

logger = logging.getLogger(__name__)


def place_order(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float = None
) -> dict:
    """
    Place a futures order on Binance Testnet.

    Args:
        symbol: Trading pair (e.g., 'BTCUSDT').
        side: 'BUY' or 'SELL'.
        order_type: 'MARKET' or 'LIMIT'.
        quantity: Order quantity.
        price: Limit price (required if order_type is 'LIMIT').

    Returns:
        dict: The raw order response from Binance.

    Raises:
        ValueError: If LIMIT order without price.
        BinanceAPIException: If Binance API returns an error.
        BinanceRequestException: For network/request issues.
        Exception: For any other unexpected error.
    """
    # Validate price for LIMIT orders
    if order_type == "LIMIT" and price is None:
        raise ValueError("Price is required for LIMIT orders.")

    client = get_futures_client()

    # Prepare parameters
    params = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
    }
    if order_type == "LIMIT":
        params["price"] = price
        # For LIMIT orders, timeInForce is required; we use GTC (Good Till Cancel)
        params["timeInForce"] = "GTC"

    logger.info(f"Placing order: {params}")
    try:
        # FuturesClient uses create_order method
        response = client.futures_create_order(**params)
        logger.info(f"Order response: {response}")
        return response
    except BinanceAPIException as e:
        logger.error(f"Binance API error: {e}")
        raise
    except BinanceRequestException as e:
        logger.error(f"Network/Request error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error placing order: {e}")
        raise