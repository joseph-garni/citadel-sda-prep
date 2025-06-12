# PANDAS essentials

# RETURNS calculations 

# Daily returns by stock symbol i/.e given price is the price each day
df['daily returns'] = df.groupby('symbol')['price'].pct_change()

# Monthly returns
df['monthly returns'] = df.groupby(['symbol', df['date'].dt.to_period('M')])['price'].last().pct_change()

# Total returns over period

df['total return to present'] = ( df.groupby('symbol')['price'].last() / df.groupby('symbol')['price'].first() - 1 )

# ROLLING calculations 

# moving averages 

df['sma_20'] = df.groupby('symbol')['price'].rolling(20).mean()
df['volatility'] = df.groupby('symbol')['daily_return'].rolling(20).std()

# reset index after rolling with groupby
df['sma_20'] = df.groupby('symbol')['price'].rolling(20).mean().reset_index(0, drop=True)

# SECTOR AGGREGATION

#sector performance metrics

sector_stats = df.groupby('sector').agg(
    {'daily_return': ['mean', 'std', 'count'], 
     'market_cap' : 'sum', 
     'volume': 'mean'}
     )

# flatten column names 

sector_stats.columns = ['avg_return', 'volatility', 'observations', 'total_mcap', 'avg_volume']