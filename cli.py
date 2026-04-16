import argparse
import os
import sys
from dotenv import load_dotenv

# Add the parent directory to sys.path to allow relative imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.validators import ValidationError, validate_order_inputs
from bot.orders import execute_trading_order
from bot.logging_config import logger

def get_interactive_inputs():
    """
    Prompts the user for trade details interactively with validation.
    Returns (symbol, side, order_type, quantity, price).
    """
    print("\n🚀 Starting Interactive Order Process")
    print("-" * 40)
    
    # Symbol with default
    symbol = input("Enter symbol (default: BTCUSDT): ").strip().upper() or "BTCUSDT"
    
    # Side validation
    side = ""
    while side not in ["BUY", "SELL"]:
        side = input("Enter side (BUY/SELL): ").strip().upper()
        if side not in ["BUY", "SELL"]:
            print("❌ Invalid side. Choose BUY or SELL.")
            
    # Order type validation
    order_type = ""
    while order_type not in ["MARKET", "LIMIT"]:
        order_type = input("Enter order type (MARKET/LIMIT): ").strip().upper()
        if order_type not in ["MARKET", "LIMIT"]:
            print("❌ Invalid type. Choose MARKET or LIMIT.")
            
    # Quantity validation
    quantity = None
    while quantity is None:
        try:
            val = input("Enter quantity: ").strip()
            if not val:
                print("❌ Quantity is required.")
                continue
            quantity = float(val)
            if quantity <= 0:
                print("❌ Quantity must be greater than 0.")
                quantity = None
        except ValueError:
            print("❌ Invalid quantity. Please enter a numeric value.")
            
    # Price validation (only for LIMIT)
    price = None
    if order_type == "LIMIT":
        while price is None:
            try:
                val = input("Enter price: ").strip()
                if not val:
                    print("❌ Price is required for LIMIT orders.")
                    continue
                price = float(val)
                if price <= 0:
                    print("❌ Price must be greater than 0.")
                    price = None
            except ValueError:
                print("❌ Invalid price. Please enter a numeric value.")
                
    return symbol, side, order_type, quantity, price

def show_order_summary(symbol, side, order_type, quantity, price):
    """
    Displays a structured order summary and handles the confirmation step.
    Returns True if user confirms, False otherwise.
    """
    print("\n==============================")
    print("ORDER SUMMARY")
    print("=============")
    print(f"\nSymbol     : {symbol}")
    print(f"Side       : {side}")
    print(f"Type       : {order_type}")
    print(f"Quantity   : {quantity}")
    if order_type == "LIMIT":
        print(f"Price      : {price}")
    print("=================")
    
    choice = input("\nConfirm order? (y/n): ").strip().lower()
    return choice == 'y'

def main():
    # Load environment variables
    load_dotenv()

    # Get API credentials
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    # Display Welcome Banner
    print("\n" + "═"*45)
    print(" ⚡ BINANCE FUTURES CLI TRADING BOT ⚡ ")
    print("═"*45)

    symbol = side = order_type = quantity = price = None

    # Determine mode: Interactive fallback if no arguments
    if len(sys.argv) == 1:
        symbol, side, order_type, quantity, price = get_interactive_inputs()
    else:
        # Note: We keep argparse for CLI support as requested
        parser = argparse.ArgumentParser(description="Binance Futures CLI Trading Bot")
        parser.add_argument("--symbol", type=str, help="Trading symbol (e.g., BTCUSDT)")
        parser.add_argument("--side", type=str, help="Order side (BUY or SELL)")
        parser.add_argument("--type", type=str, help="Order type (MARKET or LIMIT)")
        parser.add_argument("--quantity", type=float, help="Order quantity")
        parser.add_argument("--price", type=float, help="Order price (Required for LIMIT orders)")
        
        args = parser.parse_args()
        symbol, side, order_type, quantity, price = args.symbol, args.side, args.type, args.quantity, args.price

    # Validate API credentials early
    if not api_key or not api_secret:
        print("\n❌ Error: BINANCE_API_KEY and BINANCE_API_SECRET must be set in environment variables.")
        logger.error("Missing API credentials.")
        sys.exit(1)

    try:
        # Perform final validation with specific requested messages
        if not symbol:
            raise ValidationError("❌ Symbol is required.")
        if not side or side.upper() not in ['BUY', 'SELL']:
            raise ValidationError("❌ Invalid side. Choose BUY or SELL.")
        if not order_type or order_type.upper() not in ['MARKET', 'LIMIT']:
            raise ValidationError("❌ Invalid type. Choose MARKET or LIMIT.")
        if quantity is None or quantity <= 0:
            raise ValidationError("❌ Quantity must be greater than 0.")
        if order_type.upper() == 'LIMIT' and (price is None or price <= 0):
            raise ValidationError("❌ Price is required for LIMIT orders.")

        # Re-verify with central validator for depth (e.g. format checks)
        validate_order_inputs(symbol, side, order_type, quantity, price)

        # Show Order Summary & Confirmation
        if not show_order_summary(symbol, side, order_type, quantity, price):
            print("\nOrder cancelled by user")
            logger.info(f"Order cancelled by user: {symbol} {side} {quantity}")
            return

        print("\n🚀 Placing order with Binance...")
        logger.info(f"User confirmed order: {symbol} {side} {order_type} {quantity} at {price}")

        # Execute the trading order
        response = execute_trading_order(
            api_key, api_secret, symbol, side, order_type, quantity, price
        )

        # Print Clean Success Output
        print("\n✅ Order Placed Successfully!")
        print("─" * 35)
        print(f"Order ID     : {response.get('orderId')}")
        print(f"Status       : {response.get('status')}")
        print(f"Executed Qty : {response.get('executedQty')}")
        print(f"Avg Price    : {response.get('avgPrice', 'N/A')}")
        print("─" * 35)
        
        logger.info(f"Order Successful: {response.get('orderId')}")

    except ValidationError as ve:
        # Print user-friendly validation error
        print(f"\n{str(ve)}")
        logger.warning(f"Validation failed: {ve}")
    except KeyboardInterrupt:
        print("\n\n👋 Operation cancelled by user. Goodbye!")
    except Exception as e:
        # Catch-all for unexpected errors
        print(f"\n❌ An error occurred: {e}")
        # Log full traceback details for debugging
        logger.exception("Unexpected error in CLI execution")
    finally:
        print("\nSession Finished.")

if __name__ == "__main__":
    main()
