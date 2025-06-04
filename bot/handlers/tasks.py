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
        title, description, status, board_id_str, assigned_user_id_str = [part.strip() for part in raw.split(" ")]
        board_id = int(board_id_str)
        assigned_user_id = int(assigned_user_id_str)
    except Exception:
        await message.answer(
            "❗ Пример:\n/create_task Заголовок  Описание  статус  номер доски  id ответственного "
        )
        return

    data = {
        "title": title,
        "description": description,
        "status": status,
        "board_id": board_id,
        "assigned_user_id": assigned_user_id,
    }

    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.post(f"{API_URL}/tasks/", json=data, headers=headers)

    if response.status_code == 201:
        task = response.json()
        await message.answer(
            f"✅ Задача создана:\n<b>{task['title']}</b> (ID: {task['id']})"
        )
    else:
        await message.answer("❌ Не удалось создать задачу. Проверь данные.")
