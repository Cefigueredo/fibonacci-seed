# Fibonacci Seed

# Instructions

Create a `.env` file in the `app/` directory with the following content:

```bash
DB_SOURCE="postgres"
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
EMAIL_SENDER= # Add your email here
EMAIL_PASSWORD= # Add your app password here
ENVIRONMENT="development" # or "testing" for tests
API_KEY= # Add your API key here
```

You'll need to create an app password for your email account. You can do this by following the instructions [here](https://support.google.com/accounts/answer/185833?hl=en).

Run locally in Docker with the following command:
 
```bash
docker-compose up
```

You can run tests with the following command:

```bash
pytest tests/
```