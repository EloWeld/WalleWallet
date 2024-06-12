from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    user_id: int
    username: Optional[str] = None
    full_name: Optional[str] = None
    avatar_file_id: Optional[str] = None

    class Config:
        from_attributes = True


class CurrencyBase(BaseModel):
    currency_id: int
    currency_name: str

    class Config:
        from_attributes = True


class WalletBase(BaseModel):
    wallet_id: Optional[int] = None
    user_id: int
    currency_id: int
    balance: float

    class Config:
        from_attributes = True


class MessageContent(BaseModel):
    text: Optional[str] = None
    photo_url: Optional[str] = None
    button_text: Optional[str] = None
    button_url: Optional[str] = None


class TransactionBase(BaseModel):
    transaction_id: Optional[int] = None
    wallet_id: int
    amount: float
    transaction_type: str

    class Config:
        from_attributes = True
