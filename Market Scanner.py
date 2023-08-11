import yfinance as yf
import time

def market_scanner(symbol, interval):
    while True:
        try:
            # Fetch real-time data for the specified symbol
            stock_data = yf.download(symbol, interval=interval)

            # Process the data as per your scanner requirements
            # For example, you can print the current stock data
            print(stock_data.tail(1))

            # Add your scanner logic here to identify potential trade opportunities

        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")

        # Adjust the delay as per your requirements (e.g., every 5 seconds)
        time.sleep(5)

if __name__ == "__main__":
    # Define the stock symbol you want to monitor (e.g., AAPL for Apple Inc.)
    stock_symbol = input("Enter the stock symbol: ")
    print("You entered: "+ stock_symbol.upper())
    # Define the interval for data fetching (e.g., "1m" for 1 minute, "5m" for 5 minutes, "1h" for 1 hour, etc.)
    data_interval = input("Interval(minutes/m): ")
    print("Looking for data upto: "+ data_interval.lower())
    # Start the market scanner
    market_scanner(stock_symbol.upper(), data_interval.lower())

