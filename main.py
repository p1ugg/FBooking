from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from Tk import token
from aiogram.dispatcher.filters import Text
import csv
from time_docs import dict_docs

# Инециализация бота
TOKEN_API = token

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

kb_start = ReplyKeyboardMarkup(resize_keyboard=True)
kb_start.add('🔔 Запись 🛎')
kb_start.add('🕑 Расписание 🕘')
kb_start.add('☑ Наши специалисты ✅')
kb_start.add('🩺 Врач. Учётная запись 🌡')

kb_docs = ReplyKeyboardMarkup(resize_keyboard=True)

docs_sp = list()
with open('data/doc_list.csv', 'r', newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        kb_docs.add(row[0])
        docs_sp.append(row)

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



# print(docs_sp)

# 🩺🩻🌡🩹❗️❕🔅〽️🌀🕑▫️🔸🔻🔺🟢🔵⚪️🟣🔹☑️🟩🔔🕘📢‼️🛎🧬🗓📆

@dp.message_handler(commands=['start'])  # Обработчик команды /start
async def start(message: types.Message):
    beaver_center = open('data/beavercenter.jpg', 'rb')
    await message.delete()
    await bot.send_photo(message.chat.id, beaver_center, caption=greetings,reply_markup=kb_start, parse_mode='HTML')
    # await bot.send_message(chat_id=message.from_user.id, text=greetings,
    #                        reply_markup=kb_start, disable_web_page_preview=True, parse_mode='HTML')


@dp.message_handler(Text(equals='🔔 Запись 🛎'))  # Обработчик на нажатие кнопки "Запись"
async def booking(message: types.Message):
    await message.answer(
        text=f'🧬 Выберите <b>врача</b> <u>из</u> ниже представленного <u>списка</u>: 🧬',
        reply_markup=kb_docs, parse_mode="HTML")

    specalist_booking = message.text
    now = datetime.now()
    kb_date = ReplyKeyboardMarkup(resize_keyboard=True)

    for i in range(0, 8):
        a = now + timedelta(days=i)
        kb_date.add(a.strftime("%d/%m/%y"))

    @dp.message_handler()
    async def datee(message: types.Message):
        await message.answer(
            text=f'🗓 Выберите <i>удобную</i> для вас дату <u>из</u> <b>ниже представленного</b> <u>списка</u>:',
            reply_markup=kb_date, parse_mode="HTML")

        date_booking = message.text


@dp.message_handler(Text(equals='🕑 Расписание 🕘'))
async def schedule(message: types.Message):
    await message.answer(
        text=f'Выберите специалиста ниже',
        reply_markup=kb_docs)

    @dp.message_handler()
    async def vrach1(message: types.Message):
        timee = dict_docs[message.text]
        s = ''
        for j in timee.items():
            if 'Не работает' not in j[1]:
                s += f'{j[0]} - {" ".join(j[1])}\n'
            else:
                s += f'{j[0]} - {j[1]}\n'
        await message.answer(
            text=s,
            reply_markup=kb_docs)


@dp.message_handler(Text(equals='☑ Наши специалисты ✅'))
async def specialists(message: types.Message):
    await message.answer(
        text=f'Выберите специалиста ниже',
        reply_markup=kb_docs)

    @dp.message_handler()
    async def vrach(message: types.Message):
        print(message.text)
        for i in docs_sp:
            if i[0] == message.text:
                path = f'data/{i[0]}.jpg'
                photo = open(path, 'rb')
                await bot.send_photo(chat_id=message.chat.id,
                                     photo=photo,
                                     caption=f'ФИО: {i[0]}\nОбласть деятельности: {i[1]}\nВремя работы: {i[2]}',
                                     reply_markup=kb_docs)


@dp.message_handler(Text(equals='🩺 Врач. Учётная запись 🌡'))
async def account(message: types.Message):
    await message.answer(
        text=f'work',
        reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
    executor.start_polling(dp)
