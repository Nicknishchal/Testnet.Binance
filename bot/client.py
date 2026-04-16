from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from .logging_config import logger

class BinanceClient:
    """Class to interact with Binance Futures Demo API."""
    
    def __init__(self, api_key, api_secret):
        """
        Initializes the Binance client.
        
        Args:
            api_key (str): Binance API Key.
            api_secret (str): Binance API Secret.
        """
        # Initialize client with testnet=True for Demo account logic
        self.client = Client(api_key, api_secret, testnet=True)
        # Explicitly set the base URL for futures testnet
        self.client.FUTURES_URL = "https://demo-fapi.binance.com/fapi/v1"
        logger.info("Binance Futures Client initialized for Testnet.")

    def place_order(self, symbol, side, order_type, quantity, price=None):
        """
        Places a futures order.
        
        Args:
            symbol (str): Trading pair symbol.
            side (str): BUY or SELL.
            order_type (str): MARKET or LIMIT.
            quantity (float): Amount to trade.
            price (float, optional): Price for LIMIT orders.
            
        Returns:
            dict: The API response.
        """
        try:
            params = {
                'symbol': symbol.upper(),
                'side': side.upper(),
                'type': order_type.upper(),
                'quantity': quantity
            }
            
            if order_type.upper() == 'LIMIT':
                params['price'] = price
                params['timeInForce'] = 'GTC'  # Good Til Cancelled is standard for LIMIT
            
            logger.info(f"Sending order request: {params}")
            response = self.client.futures_create_order(**params)
            logger.info(f"Order response received: {response}")
            return response
            
        except BinanceAPIException as e:
            logger.error(f"Binance API Error: {e.status_code} - {e.message}")
            raise
        except BinanceOrderException as e:
            logger.error(f"Binance Order Error: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise
