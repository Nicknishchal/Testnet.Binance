from .client import BinanceClient
from .logging_config import logger

def execute_trading_order(api_key, api_secret, symbol, side, order_type, quantity, price=None):
    """
    Constructs and sends an order using the BinanceClient.
    
    Args:
        api_key (str): API Key.
        api_secret (str): API Secret.
        symbol (str): Trading pair.
        side (str): BUY/SELL.
        order_type (str): MARKET/LIMIT.
        quantity (float): Quantity.
        price (float, optional): Price for LIMIT.
        
    Returns:
        dict: The API response.
    """
    client = BinanceClient(api_key, api_secret)
    return client.place_order(symbol, side, order_type, quantity, price)
