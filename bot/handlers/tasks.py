import os

import httpx
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.tasks.states import CreateTaskState


from bot.auth.session import user_tokens

API_URL = os.getenv("API_URL", "http://localhost:8000/api")

tasks_router = Router()


@tasks_router.message(Command("create_task"))
async def start_create_task(message: Message, state: FSMContext):
    token = user_tokens.get(message.from_user.id)
    if not token:
        await message.answer("Сначала авторизуйся с помощью /login.")
        return

    await message.answer("Введите заголовок задачи:")
    await state.set_state(CreateTaskState.waiting_for_title)


@tasks_router.message(CreateTaskState.waiting_for_title)
async def get_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Введите описание задачи:")
    await state.set_state(CreateTaskState.waiting_for_description)


@tasks_router.message(CreateTaskState.waiting_for_description)
async def get_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите статус задачи (например: todo, in_progress, done):")
    await state.set_state(CreateTaskState.waiting_for_status)


@tasks_router.message(CreateTaskState.waiting_for_status)
async def get_status(message: Message, state: FSMContext):
    await state.update_data(status=message.text)
    await message.answer("Введите ID доски, к которой относится задача:")
    await state.set_state(CreateTaskState.waiting_for_board_id)


@tasks_router.message(CreateTaskState.waiting_for_board_id)
async def get_board_id(message: Message, state: FSMContext):
    try:
        board_id = int(message.text)
    except ValueError:
        await message.answer("ID доски должен быть числом.")
        return
    await state.update_data(board_id=board_id)
    await message.answer("Введите ID пользователя, которому назначена задача:")
    await state.set_state(CreateTaskState.waiting_for_assigned_user_id)


@tasks_router.message(CreateTaskState.waiting_for_assigned_user_id)
async def get_assigned_user_id(message: Message, state: FSMContext):
    try:
        assigned_user_id = int(message.text)
    except ValueError:
        await message.answer("ID пользователя должен быть числом.")
        return

    await state.update_data(assigned_user_id=assigned_user_id)
    data = await state.get_data()

    token = user_tokens.get(message.from_user.id)
    headers = {"Authorization": f"Bearer {token}"}

    task_data = {
        "title": data["title"],
        "description": data["description"],
        "status": data["status"],
        "board_id": data["board_id"],
        "assigned_user_id": data["assigned_user_id"],
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{API_URL}/tasks/", json=task_data, headers=headers)

    if response.status_code == 201:
        task = response.json()
        await message.answer(f"✅ Задача создана:\n<b>{task['title']}</b> (ID: {task['id']})")
    else:
        await message.answer("❌ Не удалось создать задачу. Проверь введённые данные.")

    await state.clear()
