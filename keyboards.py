from datetime import datetime, timedelta

from aiogram.types import ReplyKeyboardMarkup

kb_start = ReplyKeyboardMarkup(resize_keyboard=True)
kb_start.add('🔔 Запись 🛎')
kb_start.add('🕑 Расписание 🕘')
kb_start.add('☑ Наши специалисты ✅')
kb_start.add('🩺 Врач. Учётная запись 🌡')

kb_yes_or_no = ReplyKeyboardMarkup(resize_keyboard=True)
kb_yes_or_no.add('Да')
kb_yes_or_no.add('Нет')

kb_docs = ReplyKeyboardMarkup(resize_keyboard=True)
kb_date = ReplyKeyboardMarkup(resize_keyboard=True)
for i in range(0, 8):
    a = datetime.now() + timedelta(days=i)
    kb_date.add(a.strftime("%d/%m/%y"))


kb_for_doc = ReplyKeyboardMarkup(resize_keyboard=True)
kb_for_doc.add('Посмотреть мои записи')
kb_for_doc.add('Удалить запись')

kb_bookings = ReplyKeyboardMarkup(resize_keyboard=True)
