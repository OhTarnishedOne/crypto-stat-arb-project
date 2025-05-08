# Crypto Statistical Arbitrage Project

This project implements and evaluates a regime-based momentum and reversal trading strategy for major cryptocurrencies (BTC, ETH, SOL, DOGE).

## 📌 Strategy Summary

- **Momentum Strategy**: Enters long trades when volume surges in bullish + low-volatility regimes.
- **Reversal Strategy**: Enters short trades when volume surges in bearish + high-volatility regimes.
- Signals are based on lagged indicators (`sma_50`, `realized_vol`, `volume_zscore`) to avoid look-ahead bias.

## 🧪 Backtesting

- Uses a fixed holding period.
- Separates training and test data (70/30).
- Backtests are fully sequential.
- Execution costs of 20 bps are applied.

## 🔒 No Look-Ahead Bias

All signals and features are lagged, and thresholds are computed from **training data only**.

## 📊 Results

- Full strategy results are in `results/strategy_performance_summary.csv`
- Cumulative returns are plotted for both strategies
- Summary PDF: `Crypto_Stat_Arb_Project_Summary_FINAL.pdf`

## ▶️ Running the Strategy

```bash
python main_stat_arb.py
```

## 🧱 Dependencies

Install via:

```bash
pip install -r requirements.txt
```

## 📁 Structure

```
data/       → Sample crypto OHLCV data
results/    → Strategy results + equity curves
```
