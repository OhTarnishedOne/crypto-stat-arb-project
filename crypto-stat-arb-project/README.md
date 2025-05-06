
#  Crypto Statistical Arbitrage Project

This project explores statistical arbitrage opportunities in the cryptocurrency market by backtesting both momentum and reversal strategies using hourly BTC/USDT data from 20192025.

##  Strategies Tested

###  Momentum Strategy
- Volume Z-score > 1.5
- 24-hour return > +1.5%
- Only trade during bull markets (30 MA > 200 MA)
- Hold for 24 hours

###  Reversal Strategy
- Volume Z-score < -1.5
- 3-hour return < -1%
- Hold for 12 hours

##  Performance Summary

| Metric         | Momentum        | Reversal        |
|----------------|------------------|------------------|
| Sharpe Ratio   | 15.33            | -42.56           |
| CAGR           | 156.02%          | -6.57%           |
| Win Rate       | 53.85%           | 21.43%           |
| Total Trades   | 845              | 14               |
| Final Equity   | $1.88M           | $8.5K            |

##  Project Structure

- `/data/`: Raw strategy outputs and BTC price data
- `/plots/`: Equity curve comparison
- `/docs/`: Full PDF summary
- `README.md`: This file

##  Takeaway

Momentum strategies in crypto can deliver strong returns when filtered properly. Reversal strategies need refinement (possibly with liquidation, sentiment, or volatility triggers).

---
