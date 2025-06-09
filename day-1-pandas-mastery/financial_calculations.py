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
symbols = ['AAPL', 'MSTF', 'GOOGL', 'TSLA', 'NVDA', 'JPM', 'XOM', 'PG', 'XLR', 'BP', 'GS']
sector = ['Tech', 'Tech', 'Tech', 'Tech', 'Tech', 'Finance', 'Energy', 'Consumer', 'Consumer', 'Energy', 'Finance']
num_shares = ['15000000000', '7410000000', '13100000000', '3200000000', '24000000000', '24600000000', '4370000000', '2480000000', '1180000000', '4200000000']

data = []

starting_prices = [200, 290, 300, 170, 370, 170, 200, 160]

for i, symbol in enumerate(symbols):

    # More realistic - uses multiplicative returns
    dt = 1/252  # daily time step
    mu = 0.08   # annual drift
    sigma = 0.20  # annual volatility

    returns = np.random.normal(mu * dt, sigma * np.sqrt(dt), 252)
    price = starting_prices[i] * np.exp(np.cumsum(returns))
    for j, date in enumerate(dates):
        data.append({
            'symbol':symbol,
            'date': date,
            'price': int(price[j]),
            'volume': int(np.random.randint(10000000, 50000000)),
            'sector': sector[i],
            'num_shares': int(num_shares[i])
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

'''
Drill 3 - Calculating Sector Performance + Comparing Sectors

Implement:

For Each Sector:
- Average Daily Return
- Total Market Cap
- Return Volatility
- Number of Stocks
- Best Performing Stock in Each Sector

'''

drill3 = df.copy()

#calculating present market cap
drill3['market cap'] = drill3['price']*drill3['num_shares']
drill3['average daily return'] = df.groupby('symbol')['daily return'].fillna(0).mean()

# .agg(['mean', 'std', 'count']) automatically automatically maps these strings to the corresponding methods
sector_stats = drill3.groupby('symbol')['daily return'].agg(['mean', 'std', 'count']).reset_index()
sector_stats.columns = ['symbol', 'average return', 'return volatility', 'trading days']

# add sector and current market cap info
sector_stats = sector_stats.merge(latest_data[['symbol', 'sector', 'current market cap', 'volume']], on = 'symbol')

# aggregating sector metrics together in one data frame - sector metrics + rounding to 4 dp
sector_metrics = sector_stats.groupby('symbol').agg({
    'average return': 'mean',
    'return volatility': 'std',
    'current market cap': 'sum',
    'symbol': 'count',
    'volume': 'mean',
    'trading days': 'mean'
}).round(4)

# renaming sector columns for clarity
sector_metrics.columns = ['average sector returns', 'average return volatility', 'market cap', 'num stocks', 'average volume', 'average trading days']

# return best stocks
best_performers = symbol_stats.loc[symbol_stats.groupby('sector')['average return'].idxmax()]
best_performers = best_performers[['sector', 'symbol', 'average return']].rename(
    columns={'symbol': 'best stock', 'average return': 'best stock return'}
)

# combine returns for top performing stock + sector level metrics into one
sector_metrics = sector_metrics.reset_index()
sector_metrics = sector_metrics.merge(best_performs, on='sector')

print(sector_metrics)
    