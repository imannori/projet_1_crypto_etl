import json
import os
from datetime import datetime
import argparse
import time
import psycopg2
from kafka import KafkaConsumer
from dotenv import load_dotenv

load_dotenv()
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

def insert_price(symbol: str, price_usd: float, retrieved_at: datetime):
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

    conn.commit()
    cur.close()
    conn.close()


def main():

    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=int, default=60, help="Run duration in seconds")
    args = parser.parse_args()


    consumer = KafkaConsumer(
        "crypto_prices",
        bootstrap_servers=KAFKA_BOOTSTRAP,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="crypto_consumer_group",
    )

    print("✅ Consumer started... waiting for messages")

    while time.time() - start_time < args.duration:
        msg_pack = consumer.poll(timeout_ms=1000)

        for _, messages in msg_pack.items():
            for msg in messages:
                data = msg.value

                symbol = data["symbol"]
                price = float(data["price_usd"])
                retrieved_at = datetime.fromisoformat(data["retrieved_at"])

                insert_price(symbol, price, retrieved_at)
                print("✅ inserted:", data)



if __name__ == "__main__":
    main()
