"""
Input validators for CLI arguments.
"""

import re


def validate_symbol(symbol: str) -> str:
    """
    Ensure symbol is a non-empty string containing only letters and numbers.

    Args:
        symbol: Trading pair symbol (e.g., BTCUSDT).

    Returns:
        The validated symbol in uppercase.

    Raises:
        ValueError: If symbol is invalid.
    """
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Symbol must be a non-empty string.")
    symbol = symbol.strip().upper()
    if not re.match(r"^[A-Z0-9]+$", symbol):
        raise ValueError("Symbol must contain only letters and numbers (e.g., BTCUSDT).")
    return symbol


def validate_side(side: str) -> str:
    """
    Validate order side.

    Args:
        side: 'BUY' or 'SELL'.

    Returns:
        The validated side in uppercase.

    Raises:
        ValueError: If side is not BUY or SELL.
    """
    side = side.strip().upper()
    if side not in ("BUY", "SELL"):
        raise ValueError("Side must be either 'BUY' or 'SELL'.")
    return side


def validate_order_type(order_type: str) -> str:
    """
    Validate order type.

    Args:
        order_type: 'MARKET' or 'LIMIT'.

    Returns:
        The validated order type in uppercase.

    Raises:
        ValueError: If order_type is not MARKET or LIMIT.
    """
    order_type = order_type.strip().upper()
    if order_type not in ("MARKET", "LIMIT"):
        raise ValueError("Order type must be either 'MARKET' or 'LIMIT'.")
    return order_type


def validate_quantity(quantity: str) -> float:
    """
    Validate and convert quantity to positive float.

    Args:
        quantity: Quantity as string.

    Returns:
        Quantity as float.

    Raises:
        ValueError: If quantity is not a positive number.
    """
    try:
        q = float(quantity)
    except ValueError:
        raise ValueError("Quantity must be a valid number.")
    if q <= 0:
        raise ValueError("Quantity must be greater than 0.")
    return q


def validate_price(price: str) -> float:
    """
    Validate and convert price to positive float.

    Args:
        price: Price as string.

    Returns:
        Price as float.

    Raises:
        ValueError: If price is not a positive number.
    """
    try:
        p = float(price)
    except ValueError:
        raise ValueError("Price must be a valid number.")
    if p <= 0:
        raise ValueError("Price must be greater than 0.")
    return p