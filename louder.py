from aiogram.dispatcher.filters.state import StatesGroup, State


class Schedule(StatesGroup):
    sch_name = State()


class Special(StatesGroup):
    spec_name = State()

class Account(StatesGroup):
    name = State()
    password = State()
    action = State()
    del_book = State()


class Booking(StatesGroup):
    name_patient = State()
    name = State()
    date_booking = State()
    time_booking = State()
    check_true_booking = State()
