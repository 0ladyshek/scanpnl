from aiogram import types, Dispatcher
from .utils.keyboard import keyboard_main

#text="*"
async def start(message: types.Message):
    await message.answer(f"👋Добро пожаловать. Для анализа отправьте мне адрес какого-либо кошелька", reply_markup=keyboard_main)

def register(dp: Dispatcher):
    dp.register_message_handler(start)