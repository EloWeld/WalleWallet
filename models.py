from sqlalchemy import create_engine, Column, Integer, String, BigInteger, DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func
from pydantic import BaseModel

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=True)
    full_name = Column(String(100), nullable=True)
    avatar_file_id = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Currency(Base):
    __tablename__ = 'currencies'
    currency_id = Column(Integer, primary_key=True, index=True)
    currency_name = Column(String(50), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Wallet(Base):
    __tablename__ = 'wallets'
    wallet_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    currency_id = Column(Integer, ForeignKey('currencies.currency_id'), nullable=False)
    balance = Column(DECIMAL(19, 4), default=0.0)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship('User')
    currency = relationship('Currency')


class Transaction(Base):
    __tablename__ = 'transactions'
    transaction_id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey('wallets.wallet_id'), nullable=False)
    amount = Column(DECIMAL(19, 4), nullable=False)
    transaction_type = Column(String(50), nullable=False)  # 'deposit', 'withdrawal', etc.
    created_at = Column(TIMESTAMP, server_default=func.now())

    wallet = relationship('Wallet')

# Pydantic models for serialization


class UserBase(BaseModel):
    user_id: int
    username: str
    full_name: str
    avatar_file_id: str

    class Config:
        from_attributes = True


class CurrencyBase(BaseModel):
    currency_id: int
    currency_name: str

    class Config:
        from_attributes = True


class WalletBase(BaseModel):
    wallet_id: int
    user_id: int
    currency_id: int
    balance: float

    class Config:
        from_attributes = True


class TransactionBase(BaseModel):
    transaction_id: int
    wallet_id: int
    amount: float
    transaction_type: str

    class Config:
        from_attributes = True


# Database setup
DATABASE_URL = "sqlite:///./test.db"  # Example for SQLite, replace with your DB URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
