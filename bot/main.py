import asyncio
import os

import httpx
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from bot.auth.session import user_tokens
from dotenv import load_dotenv
from handlers.boards import boards_router
from handlers.tasks import tasks_router

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL", "http://localhost:8000/api")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


class LoginState(StatesGroup):
    waiting_for_credentials = State()


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я бот для работы с задачами.\nИспользуй /login чтобы авторизоваться."
    )


@dp.message(Command("login"))
async def cmd_login(message: Message, state: FSMContext):
    await message.answer("Введите логин и пароль через пробел: email password")
    await state.set_state(LoginState.waiting_for_credentials)


@dp.message(LoginState.waiting_for_credentials)
async def process_login_credentials(message: Message, state: FSMContext):
    if "@" in message.text and " " in message.text:
        try:
            email, password = message.text.strip().split(" ", 1)
        except ValueError:
            await message.answer("Неверный формат. Используй: email password")
            return

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_URL}/users/login", json={"email": email, "password": password}
            )
            if response.status_code == 200:
                token = response.json()["token"]
                user_tokens[message.from_user.id] = token
                await message.answer("✅ Авторизация успешна!")
                await state.clear()
            else:
                await message.answer("❌ Ошибка авторизации. Проверь логин и пароль.")
    else:
        await message.answer("Неверный формат. Используй: email password")


async def main():
    dp.include_routers(boards_router, tasks_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
