# Wall-E Wallet

Wall-E Wallet is a Telegram bot wallet system built with FastAPI, SQLAlchemy, Alembic, and Aiogram. It allows users to manage multiple wallets, check balances, transfer currency, and receive notifications with various types of content.

## Features

- Telegram bot integration using Aiogram 3.
- FastAPI for the REST API.
- SQLAlchemy for ORM and database interaction.
- Alembic for database migrations.
- Support for sending messages, images, documents, links, and buttons to all users.
- Docker support for easy deployment.

## Requirements

- Python 3.8+
- PostgreSQL
- Docker (optional, for containerization)

## Installation

1. **Clone the repository:**
2. **Set up a virtual environment:**
```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
3. **Install dependencies:**
```
pip install -r requirements.txt
```
4. **Create a .env file in the project root with the following content:**
```
DATABASE_URL=postgresql://user:password@localhost/dbname
TELEGRAM_TOKEN=your-telegram-bot-token
```
*Replace user, password, localhost, dbname, and your-telegram-bot-token with your actual database credentials and Telegram bot token.*
5. **Apply database migrations:**
```
alembic upgrade head
```
## Running the Project
### Running with Uvicorn
1. Start the FastAPI application:
```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
2. Start the Telegram bot:
```
python app/bot/main.py
```
## Running with Docker
Build and run the Docker containers:
```
docker-compose up --build
```

# Project structure
```
wall-e-wallet/
├── alembic/
│   ├── versions/
│   ├── env.py
│   ├── script.py.mako
│   └── alembic.ini
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── db_repository.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   ├── wallets.py
│   │   │   ├── users.py
│   │   │   ├── tg_bot_actions.py
│   ├── bot/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── handlers/
│   │   │   ├── __init__.py
│   │   │   ├── start.py
│   │   │   ├── transfers.py
│   │   │   ├── wallets.py
│   │   ├── utils.py
├── scripts/
│   ├── update_currency_rates.py
├── tests/
│   ├── __init__.py
│   ├── test_users.py
│   ├── test_wallets.py
├── Dockerfile
├── .env
├── docker-compose.yml
├── requirements.txt
└── README.md

```
