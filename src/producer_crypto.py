import json
import os
from datetime import datetime
from kafka import KafkaProducer
import requests
import time
import argparse



def fetch_price(symbol: str, retries: int = 5, backoff: int = 2) -> float:
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": symbol, "vs_currencies": "usd"}

    for attempt in range(1, retries + 1):
        r = requests.get(url, params=params, timeout=30)

        if r.status_code == 429:
            sleep_s = backoff ** attempt
            print(f"⚠️ 429 Too Many Requests ({symbol}). sleep {sleep_s}s (attempt {attempt}/{retries})")
            time.sleep(sleep_s)
            continue

        r.raise_for_status()
        data = r.json()
        return data[symbol]["usd"]

    raise RuntimeError(f"CoinGecko rate limit for {symbol} after {retries} retries")


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=int, default=60, help="Run duration in seconds")
    parser.add_argument("--interval", type=int, default=30, help="Seconds between sends")
    args = parser.parse_args()

    producer = KafkaProducer(
        bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )


    mapping = {
    "bitcoin": "btc",
    "ethereum": "eth",
    }

    start_time = time.time()
    while time.time() - start_time < args.duration:

        for coin_id in ["bitcoin", "ethereum"]:
            short = mapping[coin_id]
            price = fetch_price(coin_id)

            message = {
                "symbol": short,
                "price_usd": price,
                "retrieved_at": datetime.utcnow().isoformat(),
        }

            producer.send("crypto_prices", value=message)
            print("✅ sent:", message)

        producer.flush()
        time.sleep(args.interval)



if __name__ == "__main__":
    main()
