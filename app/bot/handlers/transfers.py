from aiogram import types, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from sqlalchemy.orm import Session
from app.database import get_db
from app.db_repository import get_wallet, create_transaction, update_wallet_balance
from app.schemas import TransactionBase
from decimal import Decimal

transfer_router = Router()


@transfer_router.message(Command("transfer"))
async def cmd_transfer(message: types.Message):
    args = message.text.split()[1:]
    if len(args) != 3:
        await message.answer("Usage: /transfer \"from_wallet_id\" \"to_wallet_id\" \"amount\"")
        return

    from_wallet_id, to_wallet_id, amount = args
    try:
        from_wallet_id = int(from_wallet_id)
        to_wallet_id = int(to_wallet_id)
        amount = Decimal(amount)
    except ValueError:
        await message.answer("❌ Invalid input. Make sure wallet IDs are integers and amount is a valid number.")
        return

    if amount <= 0:
        await message.answer("❌ The amount must be greater than zero.")
        return

    db: Session = next(get_db())
    from_wallet = get_wallet(db, wallet_id=from_wallet_id)
    to_wallet = get_wallet(db, wallet_id=to_wallet_id)

    # Many conditions
    if not from_wallet or not to_wallet:
        await message.answer("❌ Invalid wallet ID(s).")
        return

    if from_wallet.user_id != message.from_user.id:
        await message.answer("❌ You can only transfer from your own wallet.")
        return

    if from_wallet == to_wallet:
        await message.answer("❌ The wallet of sending and receiving must be different.")
        return

    if from_wallet.currency_id != to_wallet.currency_id:
        await message.answer("❌ Transfer failed: The source and destination wallets must have the same currency.")
        return

    if from_wallet.balance < amount:
        await message.answer("❌ Insufficient balance in the source wallet.")
        return

    # Perform the transfer
    from_wallet.balance -= amount
    to_wallet.balance += amount
    update_wallet_balance(db, from_wallet)
    update_wallet_balance(db, to_wallet)

    # Create transactions
    create_transaction(db, TransactionBase(wallet_id=from_wallet_id, amount=-amount, transaction_type='transfer_out'))
    create_transaction(db, TransactionBase(wallet_id=to_wallet_id, amount=amount, transaction_type='transfer_in'))

    await message.answer(f"⭐️ Successfully transferred {amount} from wallet {from_wallet_id} to wallet {to_wallet_id}.")
