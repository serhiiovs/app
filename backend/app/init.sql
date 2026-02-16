CREATE TABLE IF NOT EXISTS exchange_rates (
    rate_date DATE NOT NULL,
    currency TEXT NOT NULL,
    rate NUMERIC NOT NULL,
    PRIMARY KEY (rate_date, currency)
);
