from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from Tk import token
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import csv
from time_docs import dict_docs
from louder import Schedule, Special, Booking
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging

# -*- coding: utf-8 -*-

logging.basicConfig(level=logging.INFO)

# Инициализация бота
TOKEN_API = token

bot = Bot(TOKEN_API)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

kb_start = ReplyKeyboardMarkup(resize_keyboard=True)
kb_start.add('🔔 Запись 🛎')
kb_start.add('🕑 Расписание 🕘')
kb_start.add('☑ Наши специалисты ✅')
kb_start.add('🩺 Врач. Учётная запись 🌡')

kb_yes_or_no = ReplyKeyboardMarkup(resize_keyboard=True)
kb_yes_or_no.add('Да')
kb_yes_or_no.add('Нет')

kb_docs = ReplyKeyboardMarkup(resize_keyboard=True)
list_kb_times = []
docs_sp = list()
with open('data/doc_list.csv', 'r', newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        kb_docs.add(row[0])
        docs_sp.append(row)
print(docs_sp)


def get_dict_of_username_docs(docs_sp):
    dict_of_ids = dict()
    for row in docs_sp:
        dict_of_ids[row[0]] = row[3]

    return dict_of_ids


def get_dict_of_id_docs(docs_sp):
    dict_of_ids = dict()
    for row in docs_sp:
        dict_of_ids[row[0]] = row[4]

    return dict_of_ids


now = datetime.now()
kb_date = ReplyKeyboardMarkup(resize_keyboard=True)
for i in range(0, 8):
    a = now + timedelta(days=i)
    kb_date.add(a.strftime("%d/%m/%y"))

greetings = f'''😇 Приветствуем! 😇 \n\nВы находитесь в <u>telegram-боте</u> клиники <code>ООО"Бобёр"</code> 🦫\n
❗️Наша клиника оснащена <b>первоклассным оборудованием</b>, 
ведь счастливая жизнь пациента - это наша забота 🩻\n\n❕️Удобная инфраструктура \
здания клиники гарантирует вам <i>быстрое и понятное</i> перемещение по ней\n
‼️Лучшие специалисты страны с большим стажем работы\n
🩹 Вы можете ознакомиться \
с отзывами клиники на данном {'<a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">сайте</a>'}\n\n
🔅 Данный бот даёт возможность записаться на приём к врачу, \
а также доступ к некоторому сопутсвующему функционалу. Для\
 продолжения работы выберите одну(1) из четырёх(4) функций в меню кнопок 🔅'''


def remove_time(dict_docs, list_of_data):
    cur_list = dict_docs[list_of_data[0]][list_of_data[1]]
    cur_list.remove(list_of_data[2])
    return cur_list


# 🩺🩻🌡🩹❗️❕🔅〽️🌀🕑▫️🔸🔻🔺🟢🔵⚪️🟣🔹☑️🟩🔔🕘📢‼️🛎🧬🗓📆

@dp.message_handler(commands=['start'], state='*')  # Обработчик команды /start
async def start(message: types.Message):
    beaver_center = open('data/beavercenter.jpg', 'rb')
    await message.delete()

    await bot.send_photo(message.chat.id, beaver_center, caption=greetings, reply_markup=kb_start, parse_mode='HTML')
    # await bot.send_message(chat_id=message.from_user.id, text=greetings,
    #                        reply_markup=kb_start, disable_web_page_preview=True, parse_mode='HTML')


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    await state.finish()
    await message.reply('Отмена.', reply_markup=kb_start)


@dp.message_handler(Text(equals='🔔 Запись 🛎'), state=None)  # Обработчик на нажатие кнопки "Запись"
async def booking(message: types.Message):
    await message.answer(
        text=f'🧬 Выберите <b>врача</b> <u>из</u> ниже представленного <u>списка</u>: 🧬',
        reply_markup=kb_docs,
        parse_mode="HTML")
    await Booking.name.set()


@dp.message_handler(lambda message: [message.text] not in list(kb_docs)[0][1], state=Booking.name)
async def procces_date_invalid(message: types.Message, state: FSMContext):
    return await message.reply('Такой врач у нас не работает.\nПожалуйста, выбери врача с клавиатуры',
                               reply_markup=kb_docs)


@dp.message_handler(state=Booking.name)
async def procces_date(message: types.Message, state: FSMContext):
    async with state.proxy() as list_of_data:
        list_of_data['name'] = message.text

    await message.answer(
        text=f'🗓 Выберите <i>удобную</i> для вас дату <u>из</u> <b>ниже представленного</b> <u>списка</u>:',
        reply_markup=kb_date, parse_mode="HTML")
    await Booking.next()


@dp.message_handler(lambda message: [message.text] not in list(kb_date)[0][1], state=Booking.date_booking)
async def process_times_invalid(message: types.Message, state: FSMContext):
    return await message.reply('Выбрана неправильная дата.\nПожалуйста, выбери дату с клавиатуры', reply_markup=kb_date)


@dp.message_handler(state=Booking.date_booking)
async def process_times(message: types.Message, state: FSMContext):
    global list_kb_times
    async with state.proxy() as list_of_data:
        list_of_data['date'] = message.text

    kb_times = ReplyKeyboardMarkup(resize_keyboard=True)

    time_doc = dict_docs[list_of_data['name']][list_of_data['date']]
    if time_doc == 'Не работает':
        await message.answer(
            text=f'К сожалению, специалист не работает в этот день.\nПопробуйте выбрать другой день или поменять специалиста.',
            reply_markup=kb_start
        )
        await state.finish()

    else:
        for i in time_doc:
            kb_times.add(i)
        list_kb_times = list(kb_times)[0][1]
        await message.answer(
            text=f'Выберите удобное для Вас время',
            reply_markup=kb_times
        )
        await Booking.next()


@dp.message_handler(lambda message: [message.text] not in list_kb_times, state=Booking.time_booking)
async def process_check_true_booking_invalid(message: types.Message, state: FSMContext):
    return await message.reply('Пожалуйста, выберите корректное время с клавиатуры')


@dp.message_handler(state=Booking.time_booking)
async def process_check_true_booking(message: types.Message, state: FSMContext):
    await Booking.next()
    async with state.proxy() as list_of_data:
        list_of_data['time'] = message.text
    kb_times = ReplyKeyboardMarkup(resize_keyboard=True)
    print(list_of_data)

    await message.answer(
        text=f'Запись к врачу: {list_of_data["name"]}\nДата: {list_of_data["date"]}\nВремя: {list_of_data["time"]}\nВсе ли правильно?',
        reply_markup=kb_yes_or_no
    )


@dp.message_handler(lambda message: message.text.lower() not in ['да', 'нет'], state=Booking.check_true_booking)
async def check_result_invalid(message: types.Message, state: FSMContext):
    return await message.reply('Пожалуйста, выберите да или нет с клавиатуры',
                               reply_markup=kb_yes_or_no)


@dp.message_handler(Text(equals='Да'), state=Booking.check_true_booking)
async def check_result_yes(message: types.Message, state: FSMContext):
    async with state.proxy() as list_of_data:
        list_of_data['yes'] = message.text
    with open('data/dates_of_booking.csv', 'a', newline='', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerows([[list_of_data['name'], list_of_data['date'], list_of_data['time'], message.from_user.id]])
    new_list = remove_time(dict_docs, [list_of_data['name'], list_of_data['date'], list_of_data['time']])
    dict_docs[list_of_data['name']][list_of_data['date']] = new_list

    dict_of_username = get_dict_of_username_docs(docs_sp)
    dict_of_ids = get_dict_of_id_docs(docs_sp)

    await message.answer(
        text=f'Вы успешно записались к врачу.\nЛичная связь с врачом -> {dict_of_username[list_of_data["name"]]}',
        reply_markup=kb_start
    )
    doc_id = dict_of_ids[list_of_data['name']]
    ans = f'Оп, оп. К вам записался клиентик - @{message.from_user.username}.\nДата - {list_of_data["date"]}\nВремя - {list_of_data["time"]}'
    await bot.send_message(doc_id, ans)
    await state.finish()


@dp.message_handler(Text(equals='Нет'), state=Booking.check_true_booking)
async def check_result_yes(message: types.Message, state: FSMContext):
    await message.answer(
        text=f'Возращаю Вас в главное меню',
        reply_markup=kb_start
    )
    await state.finish()


@dp.message_handler(Text(equals='🕑 Расписание 🕘'), state=None)
async def schedule(message: types.Message):
    print(message.from_user.id)
    await message.answer(
        text=f'Выберите специалиста ниже',
        reply_markup=kb_docs)
    await Schedule.sch_name.set()


@dp.message_handler(state=Schedule.sch_name)
async def vrach1(message: types.Message, state: FSMContext):
    timee = dict_docs[message.text]
    s = ''
    for j in timee.items():
        if 'Не работает' not in j[1]:
            s += f'{j[0]} - {" ".join(j[1])}\n'
        else:
            s += f'{j[0]} - {j[1]}\n'
    await message.answer(
        text=s,
        reply_markup=kb_start)
    await state.reset_state()


@dp.message_handler(Text(equals='☑ Наши специалисты ✅'), state=None)
async def specialists(message: types.Message):
    await message.answer(
        text=f'Выберите специалиста ниже',
        reply_markup=kb_docs)
    await Special.spec_name.set()


@dp.message_handler(state=Special.spec_name)
async def vrach(message: types.Message, state: FSMContext):
    for i in docs_sp:
        if i[0] == message.text:
            try:
                path = f'data/{i[0]}.jpg'
                photo = open(path, 'rb')
            except Exception as ex:
                path = f'data/{i[0]}.png'
                photo = open(path, 'rb')
            await bot.send_photo(chat_id=message.chat.id,
                                 photo=photo,
                                 caption=f'ФИО: {i[0]}\nОбласть деятельности: {i[1]}\nВремя работы: {i[2]}',
                                 reply_markup=kb_start)
            await state.reset_state()


@dp.message_handler(Text(equals='🩺 Врач. Учётная запись 🌡'))
async def account(message: types.Message):
    await message.answer(
        text=f'work',
        reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
    executor.start_polling(dp)
