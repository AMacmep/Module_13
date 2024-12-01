# Домашнее задание по теме "Клавиатура кнопок".
# Цель: научится создавать клавиатуры и кнопки на них в Telegram-bot.


from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

api_f = open('api.txt', 'r')
api = api_f.read()
bot = Bot(token=api)
api_f.close()
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Расчитать')
button2 = KeyboardButton(text='Информация')
kb.row(button, button2)

@dp.message_handler(text='Информация')
async def inf(message):
    await message.answer('Информация о боте!')


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=["start"])
async def start(message):
    await message.answer('Привет! Я - бот, помогающий твоему здоровью.', reply_markup=kb)



@dp.message_handler(text='Расчитать')
async def set_age(message):
    await message.answer('Введите свой возраст (полных лет)')
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
