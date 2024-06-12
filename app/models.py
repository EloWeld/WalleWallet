from sqlalchemy import Column, Float, Integer, String, BigInteger, DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=True)
    full_name = Column(String(100), nullable=True)
    avatar_file_id = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Currency(Base):
    __tablename__ = 'currencies'
    currency_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    currency_name = Column(String(50), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    exchange_rate = Column(Float, nullable=True)


class Wallet(Base):
    __tablename__ = 'wallets'
    wallet_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    currency_id = Column(Integer, ForeignKey('currencies.currency_id', ondelete='CASCADE'), nullable=False)
    balance = Column(DECIMAL(19, 4), default=0.0)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship('User')
    currency = relationship('Currency')


class Transaction(Base):
    __tablename__ = 'transactions'
    transaction_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    wallet_id = Column(Integer, ForeignKey('wallets.wallet_id', ondelete='CASCADE'), nullable=False)
    amount = Column(DECIMAL(19, 4), nullable=False)
    transaction_type = Column(String(50), nullable=False)  # 'deposit', 'withdrawal', etc.
    created_at = Column(TIMESTAMP, server_default=func.now())

    wallet = relationship('Wallet')
