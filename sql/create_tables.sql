CREATE TABLE IF NOT EXISTS crypto_prices (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    price_usd NUMERIC(20, 8) NOT NULL,
    market_cap_usd NUMERIC(30, 2),
    volume_24h_usd NUMERIC(30, 2),
    retrieved_at TIMESTAMP NOT NULL
);
