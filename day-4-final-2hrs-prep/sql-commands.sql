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


    