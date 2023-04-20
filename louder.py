from aiogram.dispatcher.filters.state import StatesGroup, State


class Schedule(StatesGroup):
    sch_name = State()


class Special(StatesGroup):
    spec_name = State()
