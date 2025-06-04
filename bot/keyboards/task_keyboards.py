from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def status_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="📝 todo", callback_data="status_todo")],
        [InlineKeyboardButton(text="🚧 in_progress", callback_data="status_in_progress")],
        [InlineKeyboardButton(text="✅ done", callback_data="status_done")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
