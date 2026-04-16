class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

def validate_order_inputs(symbol, side, order_type, quantity, price):
    """
    Validates the inputs for a trading order.
    
    Args:
        symbol (str): Trading pair symbol (e.g., BTCUSDT).
        side (str): BUY or SELL.
        order_type (str): MARKET or LIMIT.
        quantity (float): Amount to trade.
        price (float): Price for LIMIT orders.
        
    Raises:
        ValidationError: If any input is invalid.
    """
    if not symbol:
        raise ValidationError("Symbol is required.")
    
    if side.upper() not in ['BUY', 'SELL']:
        raise ValidationError(f"Invalid side: {side}. Must be 'BUY' or 'SELL'.")
    
    if order_type.upper() not in ['MARKET', 'LIMIT']:
        raise ValidationError(f"Invalid type: {order_type}. Must be 'MARKET' or 'LIMIT'.")
    
    if quantity <= 0:
        raise ValidationError(f"Invalid quantity: {quantity}. Must be greater than 0.")
    
    if order_type.upper() == 'LIMIT' and (price is None or price <= 0):
        raise ValidationError("Price is required and must be greater than 0 for LIMIT orders.")
    
    return True
