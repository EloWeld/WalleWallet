from aiogram import Router, types, Dispatcher
from sqlalchemy.orm import Session
from app.database import get_db
from app.bot.main import bot
from app.db_repository import create_wallet, get_all_currencies, get_user_wallets, get_wallet, get_wallets_by_currency
from app.schemas import WalletBase
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
from aiogram.enums import ParseMode
from models import Wallet

wallets_router = Router()

WALLETS_PER_PAGE = 20


@wallets_router.message(Command("wallets"))
async def cmd_wallets(message: types.Message):
    await send_wallets_page(message.from_user.id, page=1)


@wallets_router.callback_query(F.data.startswith("wallets_page:"))
async def process_wallets_page_callback(cb_query: types.CallbackQuery):
    page = int(cb_query.data.split(":")[1])
    await send_wallets_page(cb_query.from_user.id, page, cb_query.message)
    await cb_query.answer()


async def send_wallets_page(user_id: int, page: int, edit_message: Message = None):
    db: Session = next(get_db())

    offset = (page - 1) * WALLETS_PER_PAGE
    user_wallets: list[Wallet] = get_user_wallets(db, user_id=user_id, skip=offset, limit=WALLETS_PER_PAGE + 1)

    if not user_wallets:
        await bot.send_message(user_id, "You don't have any wallets yet.")
        return

    response = "Your wallets:\n"
    for wallet in user_wallets[:WALLETS_PER_PAGE]:
        response += f"Wallet <code>#{wallet.wallet_id}</code>, Currency: <code>{wallet.currency.currency_name}</code>, Balance: <code>{wallet.balance:.2f}</code>\n"

    kb_buttons = []
    if page > 1:
        kb_buttons.append(types.InlineKeyboardButton(text="⬅️", callback_data=f"wallets_page:{page - 1}"))
    if len(user_wallets) > WALLETS_PER_PAGE:
        kb_buttons.append(types.InlineKeyboardButton(text="➡️", callback_data=f"wallets_page:{page + 1}"))
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[kb_buttons])

    if edit_message is not None:
        await edit_message.edit_text(response, reply_markup=keyboard)
    else:
        await bot.send_message(user_id, response, reply_markup=keyboard)


@wallets_router.message(Command("create_wallet"))
async def cmd_create_wallet(message: types.Message):
    user_id = message.from_user.id
    args = message.text.split()[1:]
    if len(args) != 1:
        await message.answer("Usage: /create_wallet \"currency_code\"")
        return
    currency_code = args[0]

    db: Session = next(get_db())
    currencies = get_all_currencies(db)
    currency = next((c for c in currencies if c.currency_name == currency_code), None)

    if currency:
        wallet_data = WalletBase(user_id=user_id, currency_id=currency.currency_id, balance=0.0)
        create_wallet(db, wallet=wallet_data)
        await message.answer(f"⭐️ Wallet for {currency_code} created successfully.")
    else:
        await message.answer(f"❌ Currency {currency_code} not found.")


@wallets_router.message(Command("wallet_balance"))
async def cmd_wallet_balance(message: types.Message):
    args = message.text.split()[1:]
    if len(args) != 1:
        await message.answer("Usage: /wallet_balance \"wallet_id\"")
        return

    wallet_id = args[0]
    try:
        wallet_id = int(wallet_id)
    except ValueError:
        await message.answer("Invalid wallet ID. Make sure it is an integer.")
        return

    db: Session = next(get_db())
    wallet = get_wallet(db, wallet_id=wallet_id)

    if not wallet or wallet.user_id != message.from_user.id:
        await message.answer("Invalid wallet ID or you do not own this wallet.")
        return

    response = f"Wallet <code>#{wallet.wallet_id}</code>, Currency: <code>{wallet.currency.currency_name}</code>, Balance: <code>{wallet.balance}</code>"
    await message.answer(response)


@wallets_router.message(Command("wallets_by_currency"))
async def cmd_wallets_by_currency(message: types.Message):
    args = message.text.split()[1:]
    if len(args) != 1:
        await message.answer("Usage: /wallets_by_currency \"currency_name\"")
        return

    currency_name = args[0]

    db: Session = next(get_db())
    user_id = message.from_user.id
    wallets = get_wallets_by_currency(db, user_id=user_id, currency_name=currency_name)

    if not wallets:
        await message.answer(f"You don't have any wallets with the currency {currency_name}.")
        return

    response = f"Your wallets with currency {currency_name}:\n"
    for wallet in wallets:
        response += f"Wallet <code>#{wallet.wallet_id}</code>, Balance: <code>{wallet.balance}</code>\n"

    await message.answer(response)
