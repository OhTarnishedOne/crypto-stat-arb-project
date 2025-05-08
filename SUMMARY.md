# Project Summary: Stat Arb Findings (Post Look-Ahead Bias Fix)

This file documents key insights from the updated statistical arbitrage project.

## ✅ Momentum Strategy

- Performs well even after removing look-ahead bias
- Works best in:
  - Bullish regime (`sma_50` logic)
  - Low volatility (`realized_vol` in bottom 90%)
  - Volume z-score > 2 (proxy for new info or breakout)
- Consistent with crypto’s tendency to trend during retail/institutional interest surges

## 🚫 Reversal Strategy

- Underperforms after correcting look-ahead bias
- Original reversal signal (volume surge + bearish trend + high volatility) often captures continued breakdowns, not bounces
- Previously strong results were based on forward-looking return labels

## 🧠 Interpretation

- Momentum has a real, causal edge in this setting
- Reversal may still be viable, but needs:
  - Alternative entry triggers (e.g., RSI oversold, Bollinger touches)
  - Shorter holding periods
  - Different market regimes (e.g., range-bound or sideways)

## 📍 Next Steps

- Reframe reversal logic for liquidation bounces or sentiment fade-outs
- Test faster execution logic for mean-reversion
- Potentially combine both strategies in a weighted portfolio model

See the full updated project and PDF here:  
[GitHub Repo](https://github.com/OhTarnishedOne/crypto-stat-arb-project)
