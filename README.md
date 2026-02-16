# Currency App
Currency App is a simple application that allows users to view currency exchange rates. It consists of a backend API, a frontend interface, and a cron service that updates exchange rates periodically.

## Services
- **PostgreSQL**: A relational database to store currency data.
- **Backend**: A Python Flask API that serves currency data to the frontend.
- **Frontend**: A React application that displays currency exchange rates to users.
- **Cron**: A service that runs a scheduled task to fetch and update currency exchange rates in the database.

## Environment Variables
The application uses environment variables to configure the database connection. You can set these variables in a `.env` file in the root of the project. The required variables are:
- `DB_USER`: The username for the PostgreSQL database.
- `DB_PASS`: The password for the PostgreSQL database.

## Docker Compose
To build images with cron service use:
```bash
docker-compose --profile cron build
```

To run all services use:
```bash
docker-compose --profile cron up
```
