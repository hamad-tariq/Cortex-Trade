import yfinance as yf
import pandas as pd
import time

# Import the required libraries for Sterling Trader Pro API
import requests

# Function to authenticate the API key
def authenticate_api(api_key, auth_endpoint):
    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.get(auth_endpoint, headers=headers)
    return response.status_code == 200

def calculate_ema(data, period):
    return data['Close'].ewm(span=period, adjust=False).mean()

def execute_trade(api_endpoint, api_key, symbol, price, trade_type):
    headers = {'Authorization': f'Bearer {api_key}'}
    data = {
        'symbol': symbol,
        'price': price,
        'trade_type': trade_type
    }
    
    # Replace 'YOUR_TRADE_ENDPOINT_URL' with the actual trade execution endpoint URL
    trade_endpoint = 'YOUR_TRADE_ENDPOINT_URL'
    
    response = requests.post(trade_endpoint, headers=headers, data=data)
    
    if response.status_code == 200:
        print(f"Trade executed successfully: {trade_type} {symbol} at {price:.2f}")
    else:
        print("Trade execution failed.")

def market_scanner(symbol, interval, api_key, auth_endpoint):
    while True:
        try:
            # Fetch real-time data for the specified symbol
            stock_data = yf.download(symbol, interval=interval)

            # Calculate 5-minute and 10-minute EMAs
            stock_data['EMA_5'] = calculate_ema(stock_data, 5)
            stock_data['EMA_10'] = calculate_ema(stock_data, 10)

            # Get the latest 5-minute and 10-minute EMA values
            latest_ema_5 = stock_data['EMA_5'].iloc[-1]
            latest_ema_10 = stock_data['EMA_10'].iloc[-1]

            # Fetch real-time data for the latest stock price
            stock_info = yf.Ticker(symbol)
            stock_price = stock_info.history(period="1d", interval="1m")['Close'].iloc[-1]

            # Execute buy trade when EMA_5 crosses above EMA_10
            if latest_ema_5 > latest_ema_10:
                execute_trade(auth_endpoint, api_key, symbol, stock_price, "buy")

            # Execute short trade when EMA_5 crosses below EMA_10
            elif latest_ema_5 < latest_ema_10:
                execute_trade(auth_endpoint, api_key, symbol, stock_price, "sell")

            else:
                print(f"No trade signal for {symbol}")

        except ValueError as e:
            print(f"Error fetching data for {symbol}: {e}")

        # Adjust the delay as per your requirements (e.g., every 5 seconds)
        time.sleep(5)

if __name__ == "__main__":
    while True:
        try:
            # Ask the user for the API endpoint and key
            api_endpoint = input("Enter Sterling Trader Pro API endpoint: ")
            api_key = input("Enter Sterling Trader Pro API key: ")
            
            # Authenticate the API key
            auth_endpoint = 'YOUR_AUTH_ENDPOINT_URL'  # Replace with actual auth endpoint URL
            if authenticate_api(api_key, auth_endpoint):
                print("API key authenticated successfully.")
            else:
                print("Invalid API key. Please try again.")
                continue

            choice = int(input("Enter your choice:\n1. Scan Market\n2. Generate Signal\n3. Quit\n"))
            if choice == 1:
                stock_symbol = input("Enter stock symbol to scan: ")
                data_interval = input("Enter Scan Interval: ")
                market_scanner(stock_symbol.upper(), data_interval, api_key, auth_endpoint)
            elif choice == 2:
                stock_symbol = input("Enter stock symbol to trade: ")
                stock_info = yf.Ticker(stock_symbol.upper())
                stock_price = stock_info.history(period="1d", interval="1m")['Close'].iloc[-1]
                trade_type = input("Enter trade type (buy/sell): ")
                execute_trade(auth_endpoint, api_key, stock_symbol.upper(), stock_price, trade_type)
            elif choice == 3:
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except ValueError:
            print("Invalid Input...")
