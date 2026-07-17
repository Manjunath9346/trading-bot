"""
Command-line interface for the trading bot.
"""

import argparse
import sys
import logging

from bot import validators
from bot.orders import place_order
from bot.logging_config import setup_logging
from binance.exceptions import BinanceAPIException, BinanceRequestException

# Setup logging first
setup_logging()
logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse and return command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-s", "--symbol",
        required=True,
        help="Trading pair symbol (e.g., BTCUSDT)"
    )
    parser.add_argument(
        "-b", "--side",
        required=True,
        choices=["BUY", "SELL"],
        help="Order side: BUY or SELL"
    )
    parser.add_argument(
        "-t", "--type",
        required=True,
        choices=["MARKET", "LIMIT"],
        help="Order type: MARKET or LIMIT"
    )
    parser.add_argument(
        "-q", "--quantity",
        required=True,
        help="Order quantity (e.g., 0.001)"
    )
    parser.add_argument(
        "-p", "--price",
        help="Limit price (required for LIMIT orders)"
    )
    return parser.parse_args()


def display_order_summary(order_response: dict):
    """Print a formatted summary of the order."""
    print("\n" + "=" * 50)
    print("ORDER SUMMARY")
    print("=" * 50)
    print(f"Order ID:       {order_response.get('orderId', 'N/A')}")
    print(f"Symbol:         {order_response.get('symbol', 'N/A')}")
    print(f"Side:           {order_response.get('side', 'N/A')}")
    print(f"Type:           {order_response.get('type', 'N/A')}")
    print(f"Quantity:       {order_response.get('origQty', 'N/A')}")
    print(f"Status:         {order_response.get('status', 'N/A')}")
    print(f"Executed Qty:   {order_response.get('executedQty', 'N/A')}")
    # Average price may be in 'avgPrice' field (if filled)
    avg_price = order_response.get('avgPrice', None)
    if avg_price is None:
        # Sometimes it's calculated as cumQuote / executedQty
        cum_quote = order_response.get('cumQuote', None)
        executed_qty = order_response.get('executedQty', None)
        if cum_quote and executed_qty and float(executed_qty) > 0:
            avg_price = float(cum_quote) / float(executed_qty)
    if avg_price is not None:
        print(f"Avg Price:      {avg_price}")
    else:
        print("Avg Price:      N/A")
    print("=" * 50)


def main():
    """Main execution flow."""
    args = parse_arguments()

    try:
        # Validate all inputs using validators
        symbol = validators.validate_symbol(args.symbol)
        side = validators.validate_side(args.side)
        order_type = validators.validate_order_type(args.type)
        quantity = validators.validate_quantity(args.quantity)

        # Price is required for LIMIT
        price = None
        if order_type == "LIMIT":
            if not args.price:
                logger.error("Price argument missing for LIMIT order.")
                print("Error: --price is required for LIMIT orders.")
                sys.exit(1)
            price = validators.validate_price(args.price)

        logger.info(f"Validated inputs: symbol={symbol}, side={side}, type={order_type}, "
                    f"qty={quantity}, price={price}")

        # Place the order
        response = place_order(symbol, side, order_type, quantity, price)

        # Display success and summary
        print("\n✅ Order placed successfully!")
        display_order_summary(response)

    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        print(f"\n❌ Input validation error: {ve}")
        sys.exit(1)

    except BinanceAPIException as bae:
        logger.error(f"Binance API error: {bae}")
        print(f"\n❌ Binance API error: {bae.message}")
        sys.exit(1)

    except BinanceRequestException as bre:
        logger.error(f"Network error: {bre}")
        print(f"\n❌ Network/Request error: {bre}")
        sys.exit(1)

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\n❌ An unexpected error occurred. Check logs for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()