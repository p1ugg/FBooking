from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from Tk import token
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import csv
from time_docs import dict_docs
from louder import Schedule, Special, Booking, Account
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from keyboards import kb_start, kb_yes_or_no, kb_docs, kb_date
from docs_passwords import get_password

# -*- coding: utf-8 -*-

logging.basicConfig(level=logging.INFO)

# Инициализация бота
TOKEN_API = token

bot = Bot(TOKEN_API)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

list_kb_times = list()
docs_sp = list()
with open('data/doc_list.csv', 'r', newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        kb_docs.add(row[0])
        docs_sp.append(row)


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

def get_schedule(timee):
    s = ''
    for j in timee.items():
        if 'Не работает' in j[1]:
            s += f'{j[0]} - Не работает\n'
        elif not j[1]:
            s += f'{j[0]} - Все места забрнированы\nx'
        else:
            s += f'{j[0]} - {" ".join(j[1])}\n'
    return s


@dp.message_handler(commands=['start'], state='*')  # Обработчик команды /start
async def start(message: types.Message):
    beaver_center = open('data/other_photo/beavercenter.jpg', 'rb')
    await message.delete()

    await bot.send_photo(message.chat.id, beaver_center, caption=greetings, reply_markup=kb_start, parse_mode='HTML')


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    await state.finish()
    await message.reply('⚠️<i>Возращаю</i> <b>вас</b> в главное меню', reply_markup=kb_start, parse_mode="HTML")


@dp.message_handler(Text(equals='🔔 Запись 🛎'), state=None)  # Обработчик на нажатие кнопки "Запись"
async def booking(message: types.Message):
    await message.answer(
        text=f'🧬 Выберите <b>врача</b> <u>из</u> ниже представленного <u>списка</u>: 🧬',
        reply_markup=kb_docs,
        parse_mode="HTML")
    await Booking.name.set()


@dp.message_handler(lambda message: [message.text] not in list(kb_docs)[0][1], state=Booking.name)
async def procces_date_invalid(message: types.Message, state: FSMContext):
    return await message.reply('❗ Данный вами <b>специалист не работает</b> в <code>ООО"Бобёр"</code> 🦫.\nПожалуйста, <u>выбери врача</u> с клавиатуры',
                               reply_markup=kb_docs, parse_mode="HTML")


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
    return await message.reply('❗ Выбрана <b>неверная дата.</b>\nПожалуйста, <u>выберите дату</u> с клавиатуры', reply_markup=kb_date, parse_mode="HTML")


@dp.message_handler(state=Booking.date_booking)
async def process_times(message: types.Message, state: FSMContext):
    global list_kb_times
    async with state.proxy() as list_of_data:
        list_of_data['date'] = message.text

    kb_times = ReplyKeyboardMarkup(resize_keyboard=True)

    time_doc = dict_docs[list_of_data['name']][list_of_data['date']]
    if time_doc == 'Не работает':
        await message.answer(
            text=f'❗ К сожалению, <u>специалист не работает</u> в этот день.\nПопробуйте <b>выбрать другой день</b> или <b>поменять специалиста.</b>',
            reply_markup=kb_start, parse_mode="HTML"
        )
        await state.finish()

    else:
        for i in time_doc:
            kb_times.add(i)
        list_kb_times = list(kb_times)[0][1]
        print(time_doc)
        if time_doc:
            await Booking.next()
            await message.answer(
                text=f'⏰ Выберите <i>удобное</i> для вас время <u>из</u> <b>ниже представленного</b> <u>списка</u>:',
                reply_markup=kb_times, parse_mode="HTML"
            )
        else:
            await message.answer(
                text=f'❗ К сожалению, <u>все места забронированы.</u> Попробуйте выбрать <i>другой</i> <b>день</b>',
                reply_markup=kb_start, parse_mode="HTML"
            )
            await state.finish()


@dp.message_handler(lambda message: [message.text] not in list_kb_times, state=Booking.time_booking)
async def process_check_true_booking_invalid(message: types.Message, state: FSMContext):
    return await message.reply('❗ Пожалуйста, <u>выберите</u> <b>корректное</b> <u>время</u> с клавиатуры', parse_mode="HTML")


@dp.message_handler(state=Booking.time_booking)
async def process_check_true_booking(message: types.Message, state: FSMContext):
    await Booking.next()
    async with state.proxy() as list_of_data:
        list_of_data['time'] = message.text
    kb_times = ReplyKeyboardMarkup(resize_keyboard=True)
    print(list_of_data)

    await message.answer(
        text=f'💡 Давайте <b>уточним</b> ваш <b>выбор.</b>\n<i>Вы хотите записаться к:</i> <b>{list_of_data["name"]}</b>\n<i>В эту дату:</i> <b>{list_of_data["date"]}</b>\n<i>В это время:</i> <b>{list_of_data["time"]}</b>\n<u>Все ли правильно?</u>',
        reply_markup=kb_yes_or_no, parse_mode="HTML"
    )


@dp.message_handler(lambda message: message.text.lower() not in ['да', 'нет'], state=Booking.check_true_booking)
async def check_result_invalid(message: types.Message, state: FSMContext):
    return await message.reply('❗ Пожалуйста, <b>выберите</b> <u>ДА</u> или <u>НЕТ</u> с клавиатуры',
                               reply_markup=kb_yes_or_no, parse_mode="HTML")


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
        text=f'<b>Отлично!</b>\n🎆 Поздравляю, вы <b>успешно записались на приём к врачу</b> клиники <code>ООО"Бобёр"!</code> Вы можете лично <i>связаться</i> со специалистом ➡ {dict_of_username[list_of_data["name"]]}',
        reply_markup=kb_start, parse_mode="HTML"
    )
    doc_id = dict_of_ids[list_of_data['name']]
    ans = f'💡 Оп, оп. К вам <i>записался клиентик</i> ➡ @{message.from_user.username}.\n<u>Дата</u> - <b>{list_of_data["date"]}</b>\n<u>Время</u> - <b>{list_of_data["time"]}</b>'
    if doc_id != '':
        await bot.send_message(doc_id, ans, parse_mode="HTML")
    await state.finish()


@dp.message_handler(Text(equals='Нет'), state=Booking.check_true_booking)
async def check_result_yes(message: types.Message, state: FSMContext):
    await message.answer(
        text=f'⚠️<i>Возращаю</i> <b>вас</b> в главное меню',
        reply_markup=kb_start, parse_mode="HTML"
    )
    await state.finish()


@dp.message_handler(Text(equals='🕑 Расписание 🕘'), state=None)
async def schedule(message: types.Message):
    await message.answer(
        text=f'📆 Если вы хотите узнать <b>расписание</b> одного или нескольких <u>врачей клиники</u>, <i>веберите имя</i> соответсвующего <i>специалиста</i> из <u>списка ниже.</u>\n\n'
f'Если же вы хотите <b>вернуться</b> в <i>главное меню</i>, введите /cancel на клавиатуре.',
        reply_markup=kb_docs, parse_mode="HTML")
    await Schedule.sch_name.set()


@dp.message_handler(lambda message: [message.text] not in list(kb_docs)[0][1], state=Schedule.sch_name)
async def schedule_invalid(message: types.Message, state: FSMContext):
    return await message.reply('❗ Данный вами <b>специалист не работает</b> в <code>ООО"Бобёр"</code> 🦫.\nПожалуйста, <u>выбери врача</u> с клавиатуры',
                               reply_markup=kb_docs, parse_mode="HTML")


@dp.message_handler(state=Schedule.sch_name)
async def schedule(message: types.Message, state: FSMContext):
    timee = dict_docs[message.text]
    dates_for_schedule = get_schedule(timee)
    await message.answer(
        text=dates_for_schedule,
        reply_markup=kb_start)
    await state.reset_state()


@dp.message_handler(Text(equals='☑ Наши специалисты ✅'), state=None)
async def specialists(message: types.Message):
    await message.answer(
        text=f'📍 Если вы хотите <i>ознакомиться с</i> базовой <i>информацией</i> '
             f'о <b>любом</b> из наших специалистов, просто <u>выберите</u> его <u>имя</u> из <b>списка ниже.</b>\nЕсли же вы хотите <b>вернуться</b> в <i>главное меню</i>, введите /cancel на клавиатуре.',
        reply_markup=kb_docs, parse_mode="HTML")
    await Special.spec_name.set()


@dp.message_handler(lambda message: [message.text] not in list(kb_docs)[0][1], state=Special.spec_name)
async def specialist_info_invalid(message: types.Message, state: FSMContext):
    return await message.reply('Такой врач у нас не работает.\nПожалуйста, выбери врача с клавиатуры',
                               reply_markup=kb_docs)


@dp.message_handler(state=Special.spec_name)
async def specialist_info(message: types.Message, state: FSMContext):
    for i in docs_sp:
        if i[0] == message.text:
            try:
                path = f'data/photo_docs/{i[0]}.jpg'
                photo = open(path, 'rb')
            except Exception as ex:
                path = f'data/photo_docs/{i[0]}.png'
                photo = open(path, 'rb')
            await bot.send_photo(chat_id=message.chat.id,
                                 photo=photo,
                                 caption=f'🔍 <i>ФИО:</i>      <b>{i[0]}</b>\n🎯 <i>Область деятельности:</i>      <b>{i[1]} </b>\n\n🕰 <i>Время работы:</i>      <b>{i[2]}</b>',
                                 reply_markup=kb_start, parse_mode="HTML")
            await state.reset_state()
#🎖🏅🎗🎯🎆🌇🌆🌄🩼⌛️⏳🕰💡⏰⏱🩸🦠💊📆📅🗓🗒📌📍🔍

@dp.message_handler(Text(equals='🩺 Врач. Учётная запись 🌡'), state=None)
async def account(message: types.Message):
    await Account.name.set()
    await message.answer(
        text=f'Кто ты',
        reply_markup=kb_docs)


@dp.message_handler(lambda message: [message.text] not in list(kb_docs)[0][1], state=Account.name)
async def procces_password_invalid(message: types.Message, state: FSMContext):
    return await message.reply('Такой врач у нас не работает.\nПожалуйста, выбери врача с клавиатуры',
                               reply_markup=kb_docs)


@dp.message_handler(state=Account.name)
async def procces_password(message: types.Message, state: FSMContext):
    global data
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer(text=f'Введите пароль', reply_markup=types.ReplyKeyboardRemove())
    await Account.next()


@dp.message_handler(lambda message: message.text != get_password(data['name']), state=Account.password)
async def password_invalid(message: types.Message, state: FSMContext):
    return await message.reply('Введите корректный пароль\nЧтобы выйти - cancel')


@dp.message_handler(state=Account.password)
async def password_true(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['pass'] = message.text
    await message.answer('Харош')


if __name__ == '__main__':
    executor.start_polling(dp)
