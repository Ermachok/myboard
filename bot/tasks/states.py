from aiogram.fsm.state import StatesGroup, State


class CreateTaskState(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_status = State()
    waiting_for_board_id = State()
    waiting_for_assigned_user_id = State()
