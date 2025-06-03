import os

import httpx
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.auth.session import user_tokens

API_URL = os.getenv("API_URL", "http://localhost:8000/api")

tasks_router = Router()


@tasks_router.message(Command("create_task"))
async def create_task(message: Message):
    token = user_tokens.get(message.from_user.id)
    if not token:
        await message.answer("Сначала авторизуйся с помощью /login.")
        return

    try:
        _, raw = message.text.split(" ", 1)
        title, description, board_id = [part.strip() for part in raw.split("|")]
    except Exception:
        await message.answer(
            "❗ Неверный формат.\nПример:\n/create_task Заголовок | Описание | board_id"
        )
        return

    data = {
        "title": title,
        "description": description,
        "board_id": int(board_id),
    }

    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.post(f"{API_URL}/tasks/", json=data, headers=headers)

    if response.status_code == 200:
        task = response.json()
        await message.answer(
            f"✅ Задача создана:\n<b>{task['title']}</b> (ID: {task['id']})"
        )
    else:
        await message.answer("❌ Не удалось создать задачу. Проверь данные.")
