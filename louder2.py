from aiogram.dispatcher.filters.state import StatesGroup, State


class Special(StatesGroup):
    spec_name = State()
