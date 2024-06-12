import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from app.config import settings

logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.TELEGRAM_TOKEN,
          default=DefaultBotProperties(
              parse_mode=ParseMode.HTML
          ))
dp = Dispatcher(storage=MemoryStorage())


def get_my_commands() -> list[BotCommand]:
    return [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="wallets", description="Get your wallets and balances"),
        BotCommand(command="wallet_balance", description="Get balance of a specific wallet"),
        BotCommand(command="wallets_by_currency", description="Get all wallets of a specific currency"),
        BotCommand(command="transfer", description="Transfer currency"),
        BotCommand(command="create_wallet", description="Create an additional wallet for a currency"),
    ]


async def on_startup(dispatcher):
    await set_default_commands()


async def set_default_commands():
    await bot.set_my_commands(get_my_commands())


async def main():
    from app.bot.handlers import all_routers
    dp.include_routers(
        *all_routers
    )
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
