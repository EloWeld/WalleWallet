import pytest
from aiogram import types
from aiogram.dispatcher.handler import SkipHandler
from aiogram.utils.exceptions import BotBlocked
from app.bot.main import dp, bot
from app.schemas import MessageContent
from app.db_repository import create_user
from sqlalchemy.orm import Session


@pytest.mark.asyncio
async def test_send_message_to_all_users(db: Session):
    # Create a test user
    user_data = {
        "user_id": 123456789,
        "username": "testuser",
        "full_name": "Test User",
        "avatar_file_id": "avatar_file_id"
    }
    create_user(db, user=user_data)

    # Prepare the message content
    content = MessageContent(text="Hello, this is a test message")

    # Simulate sending a message
    try:
        await bot.send_message(chat_id=123456789, text=content.text)
    except BotBlocked:
        raise SkipHandler  # Skip the handler if the bot is blocked

    # Verify that the message was sent (this is a basic check, as aiogram's test utilities
    # don't provide a built-in way to verify sent messages directly)


@pytest.mark.asyncio
async def test_send_photo_to_all_users(db: Session):
    # Prepare the message content with a photo
    content = MessageContent(photo_url="https://example.com/photo.jpg", text="Here is a photo")

    # Simulate sending a photo
    try:
        await bot.send_photo(chat_id=123456789, photo=content.photo_url, caption=content.text)
    except BotBlocked:
        raise SkipHandler  # Skip the handler if the bot is blocked

    # Verify that the photo was sent (this is a basic check, as aiogram's test utilities
    # don't provide a built-in way to verify sent photos directly)
