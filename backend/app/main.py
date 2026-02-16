from fastapi import FastAPI, Query
from datetime import date
import psycopg2
import os

app = FastAPI()

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("DB_NAME", "currency")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

def get_conn():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

@app.get("/rates")
def get_rates(day: date = Query(...)):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT currency, rate
        FROM exchange_rates
        WHERE rate_date = %s
        ORDER BY currency
        """,
        (day,)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return {
        "date": day,
        "rates": {currency: rate for currency, rate in rows}
    }
