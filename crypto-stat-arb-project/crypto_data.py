import ccxt
import pandas as pd
import time

# Initialize Binance
exchange = ccxt.binanceus()

# Config
symbol = 'BTC/USDT'
timeframe = '1h'
since = exchange.parse8601('2019-01-01T00:00:00Z')
limit = 1000  # Binance max per call

def fetch_ohlcv(symbol, timeframe, since):
    all_ohlcv = []
    while since < exchange.milliseconds():
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit)
        if not ohlcv:
            break
        all_ohlcv += ohlcv
        since = ohlcv[-1][0] + 1
        time.sleep(exchange.rateLimit / 1000)
    return all_ohlcv

# Fetch and convert
ohlcv_data = fetch_ohlcv(symbol, timeframe, since)
df = pd.DataFrame(ohlcv_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
df.set_index('datetime', inplace=True)
df.drop(columns='timestamp', inplace=True)

# Save it
df.to_csv('btc_hourly_2019_2024.csv')

# Save to CSV
output_path = 'btc_hourly_2019_2024.csv'
df.to_csv(output_path)
print(f"✅ Data saved to: {output_path}")
print(df.tail())