# PANDAS essentials

df['daily returns'] = df.groupby('symbol')['price'].pct_change()

