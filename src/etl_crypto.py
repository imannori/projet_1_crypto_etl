import requests
import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime
import logging
load_dotenv()

#logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/etl.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def fetch_price(symbol: str) -> float:
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": symbol, "vs_currencies": "usd"}

    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()

    data = r.json()
    return data[symbol]["usd"]

def insert_price(symbol: str, price_usd: float, retrieved_at: datetime):
    # ouvre la connexion DB
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO crypto_prices (symbol, price_usd, retrieved_at)
        VALUES (%s, %s, %s);
        """,
        (symbol, price_usd, retrieved_at),
    )

    # valide l’écriture
    conn.commit()
    cur.close()
    conn.close()






def main():
    # Récupère la date et l’heure actuelle en UTC / heure universelle (standard dans les systèmes)
    now = datetime.utcnow()
    mapping = {
    "bitcoin": "btc",
    "ethereum": "eth"
}
    
    for symbol in ["bitcoin", "ethereum"]:
        price = fetch_price(symbol)
        short = mapping[symbol]

        insert_price(short, price, now)
        logging.info(f"Inserted {short} price={price} at {now}")


    print("ok")
    logging.info("✅ ETL finished successfully")




if __name__ == "__main__":
    main()
