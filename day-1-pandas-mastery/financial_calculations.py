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

# UK Trading days

import yfinance as yf

import holidays

uk_holidays = holidays.UK()

# Part 1
# Create realistic Sample Data:

np.random.seed(42)

dates = pd.bdate_range('2024-01-01', periods=252, holidays=uk_holidays)
symbols = ['AAPL', 'MSTF', 'GOOGL', 'TSLA', 'NVDA', 'JPM', 'XOM', 'PG', 'XLR', 'BP', 'GS']
sector = ['Tech', 'Tech', 'Tech', 'Tech', 'Tech', 'Finance', 'Energy', 'Consumer', 'Consumer', 'Energy', 'Finance']
num_shares = ['15000000000', '7410000000', '13100000000', '3200000000', '24000000000', '24600000000', '4370000000', '2480000000', '1180000000', '4200000000', '1100000000']

data = []

starting_prices = [200, 290, 300, 170, 370, 170, 200, 160, 150, 220, 210]

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

print('drill 3:')
print(drill3)
print('sector stats:')
print(sector_stats)

'''

# add sector and current market cap info
sector_stats = sector_stats.merge(['symbol', 'sector', 'current market cap', 'volume'], on = 'symbol')

# aggregating sector metrics together in one data frame - sector metrics + rounding to 4 dp
sector_metrics = sector_stats.groupby('sector').agg({
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
sector_metrics = sector_metrics.merge(best_performers, on='sector')

print(sector_metrics)
'''

'''
Drill 4 - Clean Messy Financial Data

Implement:
- removing rows with missing critical values
- handle outlier returns i.e >20% daily moves
- ensure proper data types
- remove weekends if present
- cap extreme volume values

Key functions:
- to_datetime
- to_numeric

'''

drill4 = df.copy()

# format date column correctly
drill4['date'] = pd.to_datetime(drill4['date'])
drill4['price'] = pd.to_numeric(drill4['price'], errors='coerce')
drill4['volume'] = pd.to_numeric(drill4['volume'], errors='coerce')
drill4['daily return'] = pd.to_numeric(drill4['daily return'], errors='coerce')
drill4['price']

# use dropna, subset to not remove any rows that do not include price, volume, or num shares data
drill4 = drill4.dropna(subset=['price', 'volume', 'num_shares'])

# method to remove outlier results 
drill4 = drill4[(drill4['daily return'].abs())<0.2]

print('drill 4:')
print(drill4)

'''
Drill 5 - Calculate Key Financial Metrics

Implement:
- Calculate Sharpe Ratio (risk-adjusted returns)
- maximum drawdown
- beta (Correlation to the market)
- annualised return and volatility

'''

'''

drill5 = df.copy()

# sharpe-ratio
returns = drill5['daily return'].dropna()
risk_free_daily = 0.02 / 252 # assuming 2% risk-free rate

excess_returns = returns - risk_free_daily
sharpe_ratio = excess_returns.mean() / returns.std() * np.sqrt(252) if returns.std() > 0 else 0

# maximum drawdown (%) - what is the worst loss you would get if you bought at the worst price as a % value

cumulative = (1 + returns).cumprod()
rolling_max = cumulative.expanding().max()
drawdown = (cumulative - rolling_max) / rolling_max
max_drawdown = drawdown.min()

# using yfinance for beta calculations

# downloading S&P 500 data - common market bench

sp500_data = yf.download('^GSPC', start='2024-01-01', end='2025-01-01')
sp500_data['daily market return'] = sp500_data['Close'].pct_change() # calculating daily sp500 returns
market_return = sp500_data['daily market return'].dropna()

beta = np.cov(returns,  market_return)[0, 1] / np.var(market_return) if np.var(market_return) > 0 else 0

# annualised returns
annualised_return = returns.mean() * 252
annualised_volatility = returns.std() * np.sqrt(252)

metrics = pd.Series([sharpe_ratio, max_drawdown, beta, annualised_return, annualised_volatility, len(returns)])

print(metrics)
'''

# come back to drill 5 for pandas data frame integration - actual calculations make sense

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
