FROM python:3.11-slim

WORKDIR /app
RUN pip install requests psycopg2-binary
COPY fetch_rates.py .

CMD ["python", "fetch_rates.py"]
