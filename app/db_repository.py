from sqlalchemy.orm import Session
from sqlalchemy import insert

from app.models import User, Currency, Wallet, Transaction
from app.schemas import UserBase, CurrencyBase, WalletBase, TransactionBase


def get_all_users(db: Session):
    return db.query(User).all()


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()


def create_user(db: Session, user: UserBase):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_currency(db: Session, currency_id: int):
    return db.query(Currency).filter(Currency.currency_id == currency_id).first()


def get_all_currencies(db: Session):
    return db.query(Currency).all()


def create_currency(db: Session, currency: CurrencyBase):
    db_currency = Currency(**currency.model_dump())
    db.add(db_currency)
    db.commit()
    db.refresh(db_currency)
    return db_currency


def get_wallet(db: Session, wallet_id: int):
    return db.query(Wallet).filter(Wallet.wallet_id == wallet_id).first()


def get_wallets_by_currency(db: Session, user_id: int, currency_name: str) -> list[Wallet]:
    return db.query(Wallet).join(Currency).filter(Wallet.user_id == user_id, Currency.currency_name == currency_name).all()


def get_user_wallets(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(Wallet).filter(Wallet.user_id == user_id).offset(skip).limit(limit).all()


def get_wallets(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Wallet).filter().offset(skip).limit(limit).all()


def create_wallet(db: Session, wallet: WalletBase):
    db_wallet = Wallet(**wallet.model_dump())
    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)
    return db_wallet


def create_user_with_wallets(db: Session, user: UserBase):
    db_user = create_user(db, user)
    currencies = get_all_currencies(db)
    # Prepare bulk insert data
    wallets_data = [
        {"user_id": db_user.user_id, "currency_id": currency.currency_id, "balance": 0.0}
        for currency in currencies
    ]

    # Perform bulk insert
    db.execute(insert(Wallet).values(wallets_data))
    db.commit()
    return db_user


def get_transaction(db: Session, transaction_id: int):
    return db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()


def create_transaction(db: Session, transaction: TransactionBase):
    db_transaction = Transaction(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def update_wallet_balance(db: Session, wallet: Wallet):
    db.add(wallet)
    db.commit()
    db.refresh(wallet)
    return wallet
