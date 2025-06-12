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

# FINANCIAL CALCULATIONS

# SHARPE RATIO

def sharpe_ratio(returns, risk_free=0.02):
    excess = returns - risk_free/252
    return excess.mean() / returns.std() * np.sqrt(252)

# pretty easy, returns of stock minus risk free rate divided by total num of trading days 
# i.e trading period then return the mean of the excees divided 
# by the standard deviation of the returns multiplied by the sqrt 
# of 252

# MAX DRAWDOWN

cumulative = ( 1 + returns).cumprod()
max_dd = (cumulative / cumulative.cummax() - 1).min()

# BETA CALCULATIONS (returns used are the same)

# BETA CALCULATIONS are used to understand underlying volatility of 
# stock returns relative to market returns (uses variance)
# Beta greater than 1 = stock returns are more volatile than the market index (i.e S&P 500)
# Equal means Returns = S&P (exact same metrics i.e volatility / std)
# Less than 1 means less volatile

beta = np.cov(stock_returns, market_returns)[0, 1] / np.var(market_returns)

# DATA CLEANING

# handling missing values

df['price'] = pd.to_numeric(df['price'], errors='coerce')
df = df.dropna(subset=['price', 'volume']) # this drops rows that do not have both price and volume filled in their column values


# removing outliers

df = df[df['daily_returns'].abs() < 0.20] # remove > 20 % moves

# date conversion

df['date'] = pd.to_datetime(df['date'])

# TOP / BOTTOM SELECTION

# return top performers by sector

top_by_sector = df.groupby('sector').apply(lambda x: x.nlargest(3, 'return'))

# use nlargest/nsmallest

top_stocks = df.nlargest(10, 'total_return')
worst_stocks = df.nsmallest(5, 'sharpe_ratio')

# PANDAS DRILL COMPLETE

