from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.auth.states import LoginState
from bot.auth.session import user_tokens
import httpx
import os

API_URL = os.getenv("API_URL", "http://localhost:8000/api")

auth_router = Router()


@auth_router.message(Command("login"))
async def cmd_login(message: Message, state: FSMContext):
    await message.answer("Введите email:")
    await state.set_state(LoginState.waiting_for_credentials)


@auth_router.message(LoginState.waiting_for_credentials, F.text.contains("@"))
async def process_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text.strip())
    await message.answer("Теперь введите пароль:")
    await state.set_state(LoginState.waiting_for_credentials)


@auth_router.message(LoginState.waiting_for_credentials)
async def process_password(message: Message, state: FSMContext):
    user_data = await state.get_data()
    email = user_data.get("email")
    password = message.text.strip()

    if not email:
        await message.answer("Сначала введите email. Напишите /login снова.")
        await state.clear()
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
        await message.answer("❌ Ошибка авторизации. Попробуйте ещё раз.")
        await state.clear()
