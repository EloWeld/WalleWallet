import os
import requests
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Currency
from app.config import settings
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.binance.com/api/v3/ticker/price"


def fetch_currency_rates():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch currency rates: {response.status_code}")


def update_currency_rates(db: Session, rates: dict):
    for currency_code_usdt, rate in rates.items():
        currency_code = currency_code_usdt[:-4]
        db_currency = db.query(Currency).filter(Currency.currency_name == currency_code).first()
        if db_currency:
            db_currency.exchange_rate = rate
        else:
            db.add(Currency(currency_name=currency_code, exchange_rate=rate))
    db.commit()


def main():
    db: Session = SessionLocal()
    try:
        rates_data = fetch_currency_rates()
        rates_usdt_data = {item['symbol']: float(item['price']) for item in rates_data if item['symbol'].endswith('USDT')}
        update_currency_rates(db, rates_usdt_data)
    finally:
        db.close()


if __name__ == "__main__":
    main()
