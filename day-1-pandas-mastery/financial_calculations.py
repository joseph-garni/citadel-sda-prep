'''
Day 1 - Financial Calculations Practice
Goal: Master pandas returns and risk calculations in 12 minutes

Setting the Framing:

Goal: Write any of the 6 drills in under 5 minutes from memory

Drill 1 -> Track Daily Performance
Drill 2 -> Identify Trends and Momentum
Drill 3 -> Compare Sector Performance
Drill 4 -> Ensure Data Quality for Analysis
Drill 5 -> Calculate Investment Risk Metrics
Drill 6 -> Generate Investment Recommendations

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

starting_prices = [200, 290, 300, 170, 370, 170, 200, 160]

for i, symbol in enumerate(symbols):
    price = starting_prices[i] + np.random.randn(252).cumsum() * 0.02 * starting_prices[i]  # 2% daily volatility 
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

'''
Drill 1 - Returns Calculations
'''

df['daily return'] = df.groupby('symbol')['price'].pct_change()

# Best risk-adjusted stocks over the last year (hypothetical):

# We want the equities with the highest sharpe-ratio

sharpe_ratios = df.groupby('symbol')['daily return'].apply(
    lambda x: x.mean() / x.std() if x.std() > 0 else 0
)

print(sharpe_ratios.sort_values(ascending=False))

'''
Drill 2: Identifying Trends and Momentum 

Implement:
- Rolling Averages 
- Rolling Volatility
'''

drill2 = df.copy()

drill2['simple moving average (20 days)'] = drill2.groupby('symbol')['price'].rolling(20).mean().reset_index(0, drop = True)
drill2['simple moving average (50 days)'] = drill2.groupby('symbol')['price'].rolling(50).mean().reset_index(0, drop = True)
drill2['returns volatility (30 days)'] = drill2.groupby('symbol')['daily return'].rolling(30).std().reset_index(0, drop = True)

print(drill2)

