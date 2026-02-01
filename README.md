# Crypto ETL Pipeline (CoinGecko → PostgreSQL)

## 🎯 Objective
Build a simple Data Engineering pipeline that fetches Bitcoin and Ethereum prices from the CoinGecko API and stores them in a PostgreSQL database.

## 🧱 Tech stack
- Python (requests, psycopg2)
- PostgreSQL (Docker)
- Docker Compose
- Logging (file + console)

## 📌 Features
- Fetch BTC / ETH prices from CoinGecko
- Store data into PostgreSQL table: `crypto_prices`
- Logs saved in `logs/etl.log`

## 🗂️ Project structure
- `src/` : Python scripts (ETL)
- `sql/` : SQL scripts (tables)
- `logs/` : generated logs
- `docker-compose.yml` : PostgreSQL container

## ▶️ How to run (local)
### 1) Start PostgreSQL
```bash
docker compose up -d
```
### 2) Create table
```bash
docker exec -i crypto_postgres psql -U crypto_user -d crypto_db < sql/create_tables.sql
```
### 3) Run ETL
```bash
python src/etl_crypto.py
```


## ✅ Example output (PostgreSQL)
After running the ETL:

```sql
SELECT symbol, price_usd, retrieved_at
FROM crypto_prices
ORDER BY id DESC
LIMIT 5;
```