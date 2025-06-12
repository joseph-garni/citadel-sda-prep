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

