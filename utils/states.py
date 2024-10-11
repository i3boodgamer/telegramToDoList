from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    description = State()
    date = State()


class FormDel(StatesGroup):
    id_list = State()
