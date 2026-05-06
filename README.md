# Binance Futures Testnet Trading Bot

## Overview

This project is a CLI-based Python application that allows users to place MARKET and LIMIT orders on the Binance Futures Testnet (USDT-M). The application is designed with a modular structure, proper logging, input validation, and error handling.


---

## Features

* Place MARKET and LIMIT orders
* Support for BUY and SELL sides
* Command-line interface using argparse
* Interactive CLI mode with prompts and confirmation
* Input validation with clear error messages
* Structured logging of API requests, responses, and errors
* Environment variable support for API credentials

---

## Project Structure

```
trading_bot/
  bot/
    client.py
    orders.py
    validators.py
    logging_config.py
  cli.py
  logs/
    app.log
  README.md
  requirements.txt
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd trading_bot
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate virtual environment

For Windows:
```bash
venv\Scripts\Activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the root directory:

```env
BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_api_secret
```

---

## How to Run

### MARKET Order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### LIMIT Order (Valid Example)

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 75000
```

### LIMIT Order (Error Example)

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 65000
```

---

## Sample Output

```text
Order Summary:
Symbol     : BTCUSDT
Side       : BUY
Type       : MARKET
Quantity   : 0.01

Order Response:
orderId    : 123456
status     : NEW
executedQty: 0.0000

Final message: Success
```

---

## Interactive Mode

Run without arguments to use interactive mode:

```bash
python cli.py
```

The application will prompt for:
* Symbol
* Side
* Order type
* Quantity
* Price (for LIMIT orders)

A confirmation step is included before placing the order.

---

## Logging

Logs are stored in:
```
logs/app.log
```

Logs include:
* API request details
* API responses
* Error messages
* User actions (confirmation/cancellation)

**Note:** Log file includes both MARKET and LIMIT order executions as required.

---

## Assumptions

* Binance Futures Demo/Testnet API is used
* Orders may remain in "NEW" status due to testnet behavior
* No real funds are involved

---

## Requirements

```
python-binance==1.0.19
python-dotenv==1.0.0
requests
aiohttp==3.8.1
yarl==1.7.2
multidict==5.2.0
```

---

## Bonus Implementation

Enhanced CLI user experience:
* Interactive prompts
* Structured output formatting
* Confirmation before order execution
* Improved validation messages

---

## Notes

* Do not commit `.env` or `venv` folders to version control
* Ensure API keys are valid for Binance Futures Testnet

---

## Recommended .gitignore

```text
venv/
.env
logs/
__pycache__/
```
