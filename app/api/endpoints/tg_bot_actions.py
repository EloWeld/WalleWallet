from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.db_repository import get_all_users
from app.bot.main import bot
from app.schemas import MessageContent
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

router = APIRouter()


@router.post("/broadcast-message")
async def send_message_to_all_users(content: MessageContent, db: Session = Depends(get_db)):
    users = get_all_users(db)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")

    failed_sendings = []
    for user in users:
        try:
            keyboard = None
            if content.button_text and content.button_url:
                button = InlineKeyboardButton(text=content.button_text, url=content.button_url)
                keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])

            if content.photo_url:
                await bot.send_photo(chat_id=user.user_id, photo=content.photo_url, caption=content.text, reply_markup=keyboard)
            elif content.text:
                await bot.send_message(chat_id=user.user_id, text=content.text, reply_markup=keyboard)
        except Exception as e:
            failed_sendings.append([user.user_id, str(e)])

    return {
        "status": "Message sent to users",
        "failed_sendings_count": len(failed_sendings),
        "failed_details": failed_sendings
    }
