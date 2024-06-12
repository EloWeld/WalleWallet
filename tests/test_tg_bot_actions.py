import pytest
from aiogram import types
from aiogram.exceptions import TelegramAPIError
from app.bot.main import dp, bot
from app.schemas import MessageContent
from app.db_repository import create_user
from sqlalchemy.orm import Session
from unittest.mock import AsyncMock, patch
from app.models import User  # Adjust the import based on your project structure


TEST_TGID = 6069303965

# Test for broadcast message


def test_send_message_to_all_users(client, db):
    # Test payload
    payload = {
        "text": "Test message",
        "button_text": "Click me",
        "button_url": "https://google.com"
    }

    response = client.post("/api/v1/tg_bot_actions/broadcast-message", json=payload)
    assert response.status_code == 200
    assert response.json().get('status', None) == "Message sent to users"
