-- SQL COMMANDS

-- SQL WINDOW FUNCTIONS

-- LAG / LEAD FOR RETURNS

-- daily returns calc

SELECT symbol, date, close_price,
    LAG(close_price) OVER (PARTITION BY symbol ORDER BY date) as prev_price,
    (close_price - LAG(close_price) OVER (PARTITION BY symbol ORDER BY date)) /
    LAG(close_price) OVER (PARTITION BY symbol ORDER BY date) * 100 as daily_return
    stock_prices;

-- MOVING AVERAGES 

-- 20 DAY SMA

SELECT symbol, date, close_price,
    AVG(close_price) OVER (
        PARTITION BY symbol
        ORDER BY DATE
        ROWS BETWEEN 19 PRECEDING AND CURRENT ROW
    ) as sma_20
    FROM stock_prices;


-- RANKING FUNCTIONS 

-- RANK STOCKS BY PERFORMANCE EACH DAY

SELECT date, symbol, daily_return,
    ROW_NUMBER() OVER (PARTITION BY date ORDER BY daily_return DESC) as rank,
    RANK() OVER (PARTITION BY sector, date ORDER BY daily_return DESC) as sector_rank
FROM returns_table;

-- CUMULATIVE CALCUATIONS

-- RUNNING TOTALS AND MAX DRAWDOWN

-- uses high_watermark function to show you maxmimum close price of a symbol over a date

SELECT symbol, date, close_price,
    SUM(volume) OVER (PARTITION BY symbol ORDER BY date) as cum_volume,
    MAX(close_price) OVER (PARTITION BY symbol ORDER BY date ROWS UNBOUNDED PRECEDING) as high_watermark
FROM stock_prices;

