import os

import httpx
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.auth.session import user_tokens

API_URL = os.getenv("API_URL", "http://localhost:8000/api")

boards_router = Router()


@boards_router.message(Command("boards"))
async def get_boards(message: Message):
    token = user_tokens.get(message.from_user.id)
    if not token:
        await message.answer("Сначала авторизуйся с помощью /login.")
        return

    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get(
            f"{API_URL}/boards/?skip=0&limit=100", headers=headers
        )

    if response.status_code == 200:
        boards = response.json()
        if not boards:
            await message.answer("У тебя пока нет досок.")
        else:
            text = "\n".join(
                [f"📝 {board['title']} (ID: {board['id']})" for board in boards]
            )
            await message.answer(f"Твои доски:\n{text}")
    else:
        await message.answer("Не удалось получить доски.")
