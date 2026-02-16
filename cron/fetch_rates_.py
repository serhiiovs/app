import requests
import psycopg2
import os
from datetime import date

API_URL = "https://api.frankfurter.app/latest"
BASE = "USD"

conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "postgres"),
    dbname=os.getenv("DB_NAME", "currency"),
    user=os.getenv("DB_USER", "currency"),
    password=os.getenv("DB_PASS", "currency"),
)

cur = conn.cursor()

today = date.today().isoformat()

resp = requests.get(API_URL, params={"from": BASE})

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

rates = data["rates"]

for currency, rate in rates.items():
    cur.execute(
        """
        INSERT INTO exchange_rates (rate_date, currency, rate)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING
        """,
        (today, currency, rate)
    )

conn.commit()
cur.close()
conn.close()
