from pprint import pprint

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from Tk import token
from aiogram.dispatcher.filters import Text
import csv

TOKEN_API = token

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

kb_start = ReplyKeyboardMarkup(resize_keyboard=True)
kb_start.add('Запись')
kb_start.add('Расписание')
kb_start.add('Наши специалисты')
kb_start.add('Врач. Учётная запись')

docs_sp = list()
kb_docs = ReplyKeyboardMarkup(resize_keyboard=True)
with open('data/doc_list.csv', 'r', newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        kb_docs.add(row[0])
        docs_sp.append(row)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        text=f'Приветствую! Данный бот поможет вам легко и быстро, а самое главное удобно записаться к врачу',
        reply_markup=kb_start)


@dp.message_handler(Text(equals='Запись'))
async def booking(message: types.Message):
    await message.answer(
        text=f'work',
        reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(Text(equals='Расписание'))
async def schedule(message: types.Message):
    await message.answer(
        text=f'work',
        reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(Text(equals='Наши специалисты'))
async def specialists(message: types.Message):
    await message.answer(
        text=f'work',
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


@dp.message_handler(Text(equals='Врач. Учётная запись'))
async def account(message: types.Message):
    await message.answer(
        text=f'work',
        reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
    executor.start_polling(dp)
