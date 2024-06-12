from aiogram import types, Dispatcher, Router
from aiogram.filters import CommandStart
from sqlalchemy.orm import Session
from app.bot.main import get_my_commands
from app.db_repository import create_user_with_wallets, get_user, create_user, get_all_currencies, create_wallet

from app.database import get_db
from app.schemas import UserBase, WalletBase


start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: types.Message):
    user_id = message.from_user.id

    db: Session = next(get_db())
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        from app.bot.main import bot
        user_profile_photo: types.UserProfilePhotos = await bot.get_user_profile_photos(message.from_user.id)
        username = message.from_user.username
        full_name = message.from_user.full_name
        avatar_file_id = user_profile_photo.photos[0][0].file_id if user_profile_photo.photos else ""
        user_data = UserBase(
            user_id=user_id,
            username=username,
            full_name=full_name,
            avatar_file_id=avatar_file_id
        )
        create_user_with_wallets(db, user=user_data)

    await message.answer("Welcome to the Wallet Bot!")
    cmds = get_my_commands()
    await message.answer("Here is a list of my commands\n" + '\n'.join([f"/{x.command} — {x.description}" for x in cmds]))
