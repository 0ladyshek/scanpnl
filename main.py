from datetime import datetime

start_time = datetime.now()

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from modules import *
from config import api_token
import logging

logging.basicConfig(level=logging.INFO) 
bot = Bot(token=api_token, parse_mode="html") 
dp = Dispatcher(bot, storage=MemoryStorage())

for module in modules:
    logging.warning(f"Register module {module.__name__}")
    module.register(dp)

@dp.errors_handler()
async def error_handler(update: types.Update, exception: Exception):
    logging.error(exception)
    if update.message:
        await bot.send_message(update.message.from_user.id, f"❌Ошибка: {exception}")

logging.warning(f"Startup took {datetime.now() - start_time} seconds")
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, allowed_updates=['message', 'chat_member', 'callback_query'])