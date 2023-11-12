from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard_main = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard_main.add(KeyboardButton(f"🔎Сканирование"))