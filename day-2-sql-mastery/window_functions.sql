--===

-- Citadel Sector Data Analyst Prep - Window Function Drills (core part of this apparently)

-- Covers all 6 required window function operations for financial analysis

-- ===

-- Create main stock prices table

CREATE TABLE stock_prices (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    open_price DECIMAL(10, 2),
    close_price DECIMAL(10, 2),
    high_price DECIMAL(10, 2),
    low_price DECIMAL(10, 2),
    volume BIGINT,
    sector VARCHAR(20),
    market_cap BIGINT
)