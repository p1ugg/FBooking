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
