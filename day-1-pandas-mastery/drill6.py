'''
Drill 6 - Investment Screening and Ranking

Implements:

- Generate actionable investment ideas / decisions by screening stocks for:

- Strong momentum (20-day return > sector average)
- Good risk adjusted returns (sharpe-ratio > 1.0)
- Reasonable volatility (not in top 20% volatile stocks)
- Recent outperformance (last 30 days vs sector)
- Rank final candidates by combined score

This is meant to be what Citadel Sector Analysts do daily!

Scoring:
40% - risk adjusted returns (sharpe-ratio)
30% - momentum
20% - recent return
10% - (negative) volatility

'''

import yfinance as yf
import pandas as pd
import numpy as np

from datetime import datetime

# defining our 15 stocks across 5 sectors (3 each)

stocks = {
    'Technology': ['AAPL', 'GOOGL', 'MSFT'],
    'Healthcare': ['JNJ', 'PFE', 'UNH'],
    'Financial': ['JPM', 'BAC', 'WFC'],
    'Consumer Discretionary': ['AMZN', 'TSLA', 'HD'],
    'Energy': ['XOM', 'CVX', 'COP']
    }

all_tickers = [ticker for sector_stocks in stocks.values() for ticker in sector_stocks]

start_date = '2024-01-01'
end_date = '2024-12-31'

stock_data = yf.download(all_tickers, start = start_date, end = end_date, group_by='ticker')

print(stock_data)

