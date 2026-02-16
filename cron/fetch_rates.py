from time import time
import requests
import psycopg2
import os
from datetime import date

retries = 5
for i in range(retries):
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "postgres"),
            dbname=os.getenv("DB_NAME", "currency"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
        )
        break
    except psycopg2.OperationalError as e:
        print(f"DB connection failed ({i+1}/{retries}), retrying...")
        time.sleep(5)
else:
    print("Could not connect to database after retries")
    exit(1)


API_URL = "https://api.frankfurter.app/"
BASE = "USD"

cur = conn.cursor()

today = date.today()
start_date = today.replace(day=1).isoformat()
end_date = today.isoformat()

resp = requests.get(f"{API_URL}{start_date}..{end_date}", params={"from": BASE})

if resp.status_code != 200:
    print("HTTP error:", resp.status_code, resp.text)
    exit(1)

try:
    data = resp.json()
except Exception as e:
    print("JSON decode error:", e, resp.text)
    exit(1)

if "rates" not in data:
    print("API response error:", data)
    exit(1)

for rate_date, currencies in data["rates"].items():
    for currency, rate in currencies.items():
        cur.execute(
            """
            SELECT 1 FROM exchange_rates
            WHERE rate_date = %s AND currency = %s
            """,
            (rate_date, currency)
        )
        if cur.fetchone() is None:
            cur.execute(
                """
                INSERT INTO exchange_rates (rate_date, currency, rate)
                VALUES (%s, %s, %s)
                """,
                (rate_date, currency, rate)
            )

conn.commit()
cur.close()
conn.close()
