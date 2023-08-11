import yfinance as yf
import pandas as pd

def calculate_ema(data, period):
    return data['Close'].ewm(span=period, adjust=False).mean()

def execute_trade(symbol):
    stock_data = yf.download(symbol, period="1d", interval="5m")

    # Calculate 5-minute and 10-minute EMAs
    stock_data['EMA_5'] = calculate_ema(stock_data, 5)
    stock_data['EMA_10'] = calculate_ema(stock_data, 10)

    # Get the latest 5-minute and 10-minute EMA values
    latest_ema_5 = stock_data['EMA_5'].iloc[-1]
    latest_ema_10 = stock_data['EMA_10'].iloc[-1]

    # Fetch real-time data for the latest stock price
    stock_price = yf.download(symbol, period="1d", interval="1m")['Close'].iloc[-1]

    # Execute buy trade when EMA_5 crosses above EMA_10
    if latest_ema_5 > latest_ema_10:
        entry_price = stock_price
        take_profit = entry_price + 0.25  # You can adjust the take profit amount
        stop_loss = entry_price - 0.24    # You can adjust the stop loss amount

        print(f"Executing buy trade for {symbol} at {entry_price:.2f}")
        print(f"Take Profit: {take_profit:.2f}")
        print(f"Stop Loss: {stop_loss:.2f}")

    # Execute short trade when EMA_5 crosses below EMA_10
    elif latest_ema_5 < latest_ema_10:
        entry_price = stock_price
        take_profit = entry_price - 0.25  # You can adjust the take profit amount
        stop_loss = entry_price + 0.24    # You can adjust the stop loss amount

        print(f"Executing short trade for {symbol} at {entry_price:.2f}")
        print(f"Take Profit: {take_profit:.2f}")
        print(f"Stop Loss: {stop_loss:.2f}")

    else:
        print(f"No trade signal for {symbol}")

if __name__ == "__main__":
    # Define the stock symbol you want to trade
    stock_symbol = input("Enter stock symbol: ")
    print("Let's trade in: " + stock_symbol.upper())

    # Execute the trade based on the specified criteria
    execute_trade(stock_symbol.upper())
