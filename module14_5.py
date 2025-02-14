from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from crud_functions import *

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_calculate = KeyboardButton(text='Расчитать')
button_info = KeyboardButton(text='Информация')
button_buy = KeyboardButton(text='Купить')
button_registration = KeyboardButton(text='Регистрация')
kb.row(button_calculate, button_info)
kb.add(button_buy, button_registration)

kb_inl = InlineKeyboardMarkup(resize_keyboard=True)
button_inl_cul = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_inl_info = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb_inl.row(button_inl_cul, button_inl_info)

kb_inl_buy = InlineKeyboardMarkup(resize_keyboard=True)
kb_inl_poduct1 = InlineKeyboardButton(text='Продукт 1', callback_data='product_buying')
kb_inl_poduct2 = InlineKeyboardButton(text='Продукт 2', callback_data='product_buying')
kb_inl_poduct3 = InlineKeyboardButton(text='Продукт 3', callback_data='product_buying')
kb_inl_poduct4 = InlineKeyboardButton(text='Продукт 4', callback_data='product_buying')
kb_inl_buy.row(kb_inl_poduct1, kb_inl_poduct2, kb_inl_poduct3, kb_inl_poduct4)

@dp.message_handler(text=['Расчитать'])
async def main_menu(msg):
    await msg.answer('Выберите опцию:', reply_markup=kb_inl)

@dp.message_handler(text='Купить')
async def get_buying_list(msg):
    base_products = get_all_products()
    for i in base_products:
        await msg.answer(f'Название: Продукт {i[1]}| Описание: описание{i[2]}| Цена: {i[3]}')
        with open(f'photo/{i[0]}.png', 'rb') as img:
            await msg.answer_photo(img)
    await msg.answer('Выберите продукт для покупки:', reply_markup=kb_inl_buy)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = 1000
@dp.message_handler(text='Регистрация')
async def sing_up(msg):
    await msg.answer('Введите имя пользователя (только латинский алфавит) :')
    await RegistrationState.username.set()

@dp.message_handler(state = RegistrationState.username)
async def set_username(msg, state):
    if is_included(msg.text) == False:
        await state.update_data(username = msg.text)
        await msg.answer("Введите свой email:" )
        await RegistrationState.email.set()
    else:
        await msg.answer('Пользователь существует, введите другое имя')
        await RegistrationState.username.set()

@dp.message_handler(state = RegistrationState.email)
async def set_email(msg, state):
    await state.update_data(email = msg.text)
    await msg.answer("Введите свой возраст:")
    await RegistrationState.age.set()

@dp.message_handler(state = RegistrationState.age)
async def set_age(msg, state):
    await state.update_data(age = msg.text)
    data = await state.get_data()
    add_user(data['username'], data['email'], data['age'], RegistrationState.balance)
    await msg.answer(f' Ваша регистрация прошла успешно !')
    await state.finish()

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст : ')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(msg, state):
    await state.update_data(age=msg.text)
    data = await state.get_data()
    await msg.answer('Введите свой рост : ')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(msg, state):
    await state.update_data(growth=msg.text)
    data = await state.get_data()
    await msg.answer('Введите свой вес : ')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(msg, state):
    await state.update_data(weight=msg.text)
    data = await state.get_data()
    caloris = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) + 5
    await msg.answer(f' Ваша норма калорий {caloris:.2f} ')
    await state.finish()

@dp.message_handler(text=['Привет', 'привет', 'Hi', 'hi', 'Хай', 'хай'])
async def urban_messsge(msg):
    await msg.answer('Рады вас видеть в нашем боте !')

@dp.message_handler(commands=['start'])
async def start_message(msg: types.Message):
    await msg.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=kb)

@dp.message_handler()
async def all_message(msg):
    await msg.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    #	get_all_products()
    executor.start_polling(dp, skip_updates=True)