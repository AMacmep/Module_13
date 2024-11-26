# Домашнее задание по теме "Методы отправки сообщений".
# Цель: написать простейшего телеграм-бота, используя асинхронные функции.

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

api = '7950905280:AAHFPqfPnN0hwTwp3wguU9_fd3eFGiA75Uk'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=["start"])
async def start(message):
    await message.answer('Привет! Я - бот, помогающий твоему здоровью.')


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)