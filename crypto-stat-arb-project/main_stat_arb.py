import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Setup
# -----------------------------
BASE_DIR = os.path.expanduser("~/Projects/Crypto_Stat_Arb_Project")
DATA_DIR = os.path.join(BASE_DIR, "data")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "DOGEUSDT"]
results_summary = []

# -----------------------------
# Functions
# -----------------------------
def load_data(symbol):
    filepath = os.path.join(DATA_DIR, f"{symbol}.csv")
    df = pd.read_csv(filepath, parse_dates=["timestamp"])
    df.set_index("timestamp", inplace=True)
    return df

def calculate_features(df):
    df["returns"] = df["close"].pct_change()
    df["sma_50"] = df["close"].rolling(window=50).mean()
    df["realized_vol"] = df["returns"].rolling(window=14).std()
    df["volume_zscore"] = (df["volume"] - df["volume"].rolling(window=30).mean()) / df["volume"].rolling(window=30).std()
    return df

def generate_signals(df):
    df["regime"] = np.where(df["close"] > df["sma_50"], "bullish", "bearish")
    vol_thresh = df["realized_vol"].quantile(0.9)
    df["volatility_regime"] = np.where(df["realized_vol"] > vol_thresh, "high_vol", "low_vol")
    
    df["signal"] = "none"
    df.loc[(df["volume_zscore"] > 2) & (df["regime"] == "bullish") & (df["volatility_regime"] == "low_vol"), "signal"] = "momentum"
    df.loc[(df["volume_zscore"] > 2) & (df["regime"] == "bearish") & (df["volatility_regime"] == "high_vol"), "signal"] = "reversal"
    return df

def backtest(df, signal_type, hold_period=3):
    trades = []
    signal_df = df[df["signal"] == signal_type]
    
    for i in range(len(signal_df) - hold_period):
        entry = signal_df.iloc[i]["close"]
        exit = signal_df.iloc[i + hold_period]["close"]
        direction = 1 if signal_type == "momentum" else -1
        gross = direction * (exit - entry) / entry
        net = gross - 0.002  # 20 bps execution cost
        trades.append(net)
        
    return np.array(trades)

def evaluate_performance(trades, strategy_name):
    if len(trades) == 0:
        results_summary.append({
            "Strategy": strategy_name,
            "Total Return": "N/A",
            "Sharpe": "N/A",
            "Max Drawdown": "N/A"
        })
        return
    
    cumulative_return = np.cumprod(1 + trades) - 1
    sharpe = np.mean(trades) / np.std(trades) * np.sqrt(252) if np.std(trades) > 0 else 0
    max_dd = np.min(cumulative_return - np.maximum.accumulate(cumulative_return))
    total_return = cumulative_return[-1]

    # Append to summary table
    results_summary.append({
        "Strategy": strategy_name,
        "Total Return": f"{total_return:.2%}",
        "Sharpe": f"{sharpe:.2f}",
        "Max Drawdown": f"{max_dd:.2%}"
    })

    # Save equity curve plot
    plt.figure(figsize=(8, 4))
    plt.plot(cumulative_return, label=strategy_name)
    plt.title(f"{strategy_name} Equity Curve")
    plt.xlabel("Trade #")
    plt.ylabel("Cumulative Return")
    plt.legend()
    plt.grid(True)
    filename = os.path.join(RESULTS_DIR, f"{strategy_name}_cumulative_return.png")
    plt.savefig(filename)
    plt.close()

# -----------------------------
# Main Execution
# -----------------------------
def main():
    for symbol in symbols:
        print(f"\nProcessing {symbol}...")
        df = load_data(symbol)
        df = calculate_features(df)
        df = generate_signals(df)

        for sig in ["momentum", "reversal"]:
            trades = backtest(df, sig)
            evaluate_performance(trades, f"{symbol}_{sig}")

    # Export performance summary
    summary_df = pd.DataFrame(results_summary)
    summary_path = os.path.join(RESULTS_DIR, "strategy_performance_summary.csv")
    summary_df.to_csv(summary_path, index=False)
    print(f"\n📊 Summary saved to: {summary_path}")

if __name__ == "__main__":
    main()