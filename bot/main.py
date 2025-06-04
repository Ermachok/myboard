import asyncio
import os


from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command


from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from dotenv import load_dotenv
from handlers.boards import boards_router
from handlers.tasks import tasks_router
from auth.handlers import auth_router


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL", "http://localhost:8000/api")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я бот для работы с задачами.\nИспользуй /login чтобы авторизоваться."
    )


async def main():
    dp.include_routers(auth_router, boards_router, tasks_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
