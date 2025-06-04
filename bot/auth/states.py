from aiogram.fsm.state import State, StatesGroup

class LoginState(StatesGroup):
    waiting_for_credentials = State()
