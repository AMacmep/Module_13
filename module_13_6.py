# Домашнее задание по теме "Инлайн клавиатуры".
# Цель: научится создавать Inline клавиатуры и кнопки на них в Telegram-bot.


from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api_f = open('api.txt', 'r')
api = api_f.read()
bot = Bot(token=api)
api_f.close()
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Расчитать')
button2 = KeyboardButton(text='Информация')
kb.add(button, button2)

ikb = InlineKeyboardMarkup(resize_keyboard=True)
ibutton1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
ibutton2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
ikb.add(ibutton1, ibutton2)


@dp.message_handler(text='Информация')
async def inf(message):
    await message.answer('Информация о боте!')


@dp.message_handler(commands=["start"])
async def start(message):
    await message.answer('Привет! Я - бот, помогающий твоему здоровью.', reply_markup=kb)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text='Расчитать')
async def main_menu(message):
    await message.answer('Выбрите опцию: ', reply_markup=ikb)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('Расчёт каллорий производится по формуле: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст (полных лет)')
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост, см')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес, кг')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    try:
        calories = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
        await message.answer(f'Ваши калории {calories}')
    except ValueError:
        await message.answer(
            'Данные введены некорректно. Введите числовые значения: полных лет, рост в сантиметрах, вес в килограммах')
    await state.finish()


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
