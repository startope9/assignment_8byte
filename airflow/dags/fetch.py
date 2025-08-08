import os
import requests
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime, timezone

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_USER = os.getenv("POSTGRES_USER", "airflow")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "airflow")
DB_NAME = os.getenv("PIPELINE_DB", "stocks")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DEFAULT_SYMBOL = os.getenv("SYMBOL", "AAPL")

def fetch_data(symbol=DEFAULT_SYMBOL):
    try:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()

        if "Time Series (Daily)" not in data:
            raise ValueError(f"Unexpected API response: {dict((k, data.get(k)) for k in data.keys())}")

        records = []
        for date, values in data["Time Series (Daily)"].items():
            try:
                records.append((
                    symbol,
                    date,
                    float(values.get("1. open", 0.0)),
                    float(values.get("2. high", 0.0)),
                    float(values.get("3. low", 0.0)),
                    float(values.get("4. close", 0.0)),
                    int(float(values.get("5. volume", 0) or 0))
                ))
            except Exception as e:
                print(f"[{datetime.now(timezone.utc).isoformat()}] Skipping row for {date}: {e}")
                continue
        return records
    except Exception as e:
        print(f"[{datetime.now(timezone.utc).isoformat()}] Error fetching data: {e}")
        return []

def store_data(records):
    if not records:
        print(f"[{datetime.now(timezone.utc).isoformat()}] No data to insert.")
        return

    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME,
            user=DB_USER, password=DB_PASSWORD, port=DB_PORT
        )
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS stock_prices (
                symbol TEXT,
                date DATE,
                open FLOAT,
                high FLOAT,
                low FLOAT,
                close FLOAT,
                volume BIGINT,
                PRIMARY KEY (symbol, date)
            )
        """)

        insert_query = """
            INSERT INTO stock_prices (symbol, date, open, high, low, close, volume)
            VALUES %s
            ON CONFLICT (symbol, date) DO NOTHING
        """
        execute_values(cur, insert_query, records)
        conn.commit()
        cur.close()
        print(f"[{datetime.now(timezone.utc).isoformat()}] Inserted {len(records)} records (duplicates ignored).")
    except Exception as e:
        print(f"[{datetime.now(timezone.utc).isoformat()}] Error inserting data: {e}")
    finally:
        if conn:
            conn.close()

def fetch_and_store():
    records = fetch_data()
    store_data(records)

if __name__ == "__main__":
    fetch_and_store()