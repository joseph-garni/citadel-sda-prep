'''
Day 1 - Financial Calculations Practice
Goal: Master pandas returns and risk calculations in 12 minutes
'''

import pandas as pd
import numpy as np

# Part 1
# Create realistic Sample Data:

np.random.seed(42)

dates = pd.date_range('2024-01-01', periods=252) # periods in a trading year
symbols = ['AAPL', 'MSTF', 'GOOGL', 'TSLA', 'NVDA', 'JPM', 'XOM', 'PG']
sectors = ['Tech', 'Tech', 'Tech', 'Tech', 'Tech', 'Finance', 'Energy', 'Consumer']

data = []

for i, symbol in enumerate(symbols):
    price = 100 + np.random.randn(252).cumsum() * 0.02  # 2% daily volatility 
    for j, date in enumerate(dates):
        data.append({
            'symbol':symbol,
            'date': date,
            'price': price[j],
            'volume': np.random.randint(10000000, 50000000),
            'sector': sectors[i]
        })

df = pd.DataFrame(data)
print(f"Created dataset:{df.shape}")
print(df.head())
