import asyncio
import os

import httpx
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

API_URL = "http://localhost:8000/api"
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()

# Временный storage токена (в будущем — сессии/БД)
token: str | None = None


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я бот для работы с задачами. Используй /login чтобы авторизоваться."
    )


@dp.message(Command("login"))
async def cmd_login(message: Message):
    await message.answer(
        "Введите логин и пароль через пробел: <email> <password>", parse_mode=None
    )


@dp.message()
async def handle_login_or_command(message: Message):
    global token
    if "@" in message.text and " " in message.text:
        try:
            email, password = message.text.strip().split(" ", 1)
        except ValueError:
            await message.answer("Неверный формат. Используй: <email> <password>")
            return

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_URL}/users/login", json={"email": email, "password": password}
            )
            if response.status_code == 200:
                token = response.json()["token"]
                await message.answer("✅ Авторизация успешна!")
            else:
                await message.answer("❌ Ошибка авторизации. Проверь логин и пароль.")
    elif message.text.startswith("/boards"):
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
    else:
        await message.answer("Неизвестная команда или сообщение.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
