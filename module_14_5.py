from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import get_all_products, initiate_db, is_included, add_user
import re

db_name = 'not_telegram.db'
tbl1_name = 'Products'
tbl2_name = 'Users'

class UserState(StatesGroup):
    name = State()      # Имя
    age = State()       # Возраст
    growth = State()    # Рост
    weight = State()    # Вес


class RegistrationState(StatesGroup):
    username = State()      # Имя
    email = State()       # Почта
    age = State()    # Возраст
    balance = State()    # Баланс

# Создаем клавиатуры.

# Основная клавиатура.
# Запускается при старте бота.
kb = ReplyKeyboardMarkup(resize_keyboard=True)  #  Создаем клавиатуру
bt_info = KeyboardButton(text='Информация')  # Создаем Кнопку1
bt_go = KeyboardButton(text='Рассчитать')  # Создаем Кнопку2
bt_buy = KeyboardButton(text='Купить')  # Создаем Кнопку3
bt_reg = KeyboardButton(text='Регистрация')  # Создаем Кнопку4
kb.add(bt_go, bt_info)  # Добавили две кнопки в первый ряд
kb.add(bt_buy, bt_reg)  # И две в следующий ряд

# Инлай клавиатура для расчета калорий.
# Запускается при нажатии кнопки "Рассчитать"
ikb = InlineKeyboardMarkup(resize_keyboard=True)  # Клавиатура для Рассчитать
ibt_info = InlineKeyboardButton(text='Формула расчета', callback_data='formulas')
ibt_go = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
ikb.add(ibt_go, ibt_info)

# Инлайн клавиатуры для покупок создаются при выводе списка покупок
# в методе get_buying_list().

api = "7894373187:AAG6EizTKiQDfLof5qLUszC9oeTyDhckb6k"
bot = Bot(token=api)  # Бот
dp = Dispatcher(bot, storage=MemoryStorage())  # Диспетчер

# Реакция на команду "/start".
# Выводит приветствие и запускает основную клавиатуру.
@dp.message_handler(commands='start')
async def start(message):
    await message.answer('Здравствуйте.')
    await message.answer('Я бот, который расчитает для Вас необходимое количество калорий в сутки.', reply_markup=kb)
    await message.answer('Для начала расчета, получения информации или покупок воспользуйтесь кнопками внизу экрана.')

#==================================== Обработка команды "Регистрация" =========================================
@dp.message_handler(text='Регистрация')
async def sing_up(message):
   await message.answer('Сообщите пожалуйста свое имя. Только латинские буквы.')
   await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if (re.match(r'^[a-zA-Z0-9]+$', message.text)) and (not is_included(db_name, tbl2_name, message.text)):
        await state.update_data(username=message.text)
        data = await state.get_data()
        await message.answer(f'Здравствуйте {data["username"]}')
        await message.answer('Сообщите свой email.')
        await RegistrationState.email.set()
    else:
        await message.answer('Имя введено неверно.')
        if is_included(db_name, tbl2_name, message.text):
            await message.answer('Пользователь с таким именем уже существует.')
        await message.answer('Сообщите пожалуйста свое имя. Только латинские буквы.')
        await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    data = await state.get_data()
    await message.answer(f'email {data["email"]}')
    await message.answer('Сообщите свой возраст.')
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    await message.answer(f'{data["username"]}, {data["email"]}, {data["age"]}')
    await state.finish()
    if add_user(db_name, tbl2_name, data["username"], data["email"], data["age"]):
        await message.answer('Данные успешно добавлены.')
    else:
        await message.answer('Чтото пошло не так. Вернитесь к регистрации.')

#==================================== Конец обработки команды "Зарегистрироваться" ===================================

#==================================== Обработка команды "Купить" ============================================
# Реакция на нажатие кнопки "Купить".
# Выводит название продукта, его фото, описание и цену.
# Создает инлайн клавиатуру для каждой покупки.
@dp.message_handler(text='Купить')
async def get_buying_list(message):

    for i in all_prd:
        with open(i[4], 'rb') as p1:
            t_kb = InlineKeyboardMarkup(resize_keyboard=True)
            t_kb_p1 = InlineKeyboardButton(text=f'Купить {i[1]}', callback_data='product_buying')
            t_kb_p2 = InlineKeyboardButton(text=f'Информация {i[1]}', callback_data='product_info')
            t_kb.add(t_kb_p1, t_kb_p2)
            await message.answer_photo(p1, f'Название: {i[1]} | Описание: {i[2]} | Цена: {i[3]}', reply_markup=t_kb)

# Реакция на нажатие кнопки "Купить" любой из клавиатур для покупок.
# Выводит сообщение об успешной покупке.
@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    print(call)
    await call.message.answer(f'Вы успешно приобрели продукт! {call["message"]["caption"]}')
    await call.answer()

# Реакция на нажатие кнопки "Информация" любой из клавиатур для покупок.
# Выводит информацию.
@dp.callback_query_handler(text='product_info')
async def send_confirm_message(call):
    print(call)
    await call.message.answer(f'Вы получили информацию о продукте! {call["message"]["caption"]}')
    await call.answer()
#==================================== Конец обработки команды "Купить" ============================================

#==================================== Обработка команды "Информация" ============================================
# Реакция на нажатие кнопки "Информация".
# Выводит сообщение о боте.
@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Я бот, который расчитает для Вас необходимое количество калорий в сутки.')
#==================================== Конец обработки команды "Информация" ============================================

#==================================== Обработка команды "Рассчитать" ============================================
# Реакция на нажатие кнопки "Рассчитать".
# Предлагает выбрать опцию и запускает инлайн клавиатуру для расчета калорий.
@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup=ikb)

# Реакция на на жатие кнопки "formulas".
# Выводит формулу расчета калорий.
@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()

# Реакция на на жатие кнопки "calories".
@dp.callback_query_handler(text='calories')
async def set_name(call):
    await call.message.answer('Сообщите пожалуйста свое имя.')
    await UserState.name.set()
    await call.answer()

# Последующий скрипт собирает информацию о пользователе и выводит его калории.

@dp.message_handler(state=UserState.name)
async def set_age(message, state):
    await state.update_data(name=message.text)
    data = await state.get_data()
    await message.answer(f'Здравствуйте {data["name"]}')
    await message.answer('Сообщите свой возраст (от 1 до 200 лет).')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    data = await state.get_data()
    await message.answer(f'{data["name"]}, {data["age"]}лет.')
    await message.answer('Сообщите свой вес (от 1 до 300кг).')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
    data = await state.get_data()
    await message.answer(f'{data["name"]}, {data["age"]}лет, {data["growth"]}кг.')
    await message.answer('Сообщите свой рост (от 1 до 300 см).')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    await message.answer(f'{data["name"]}, {data["age"]}лет, {data["growth"]}кг, {data["weight"]}см.')
    await message.answer(f'{data["name"]}, ваша норма калорий:'
                         f'{(10*data["growth"])+(6.25*data["weight"])-(5*data["age"])+5} кал/сутки.')
    await state.finish()
#==================================== Конец обработки команды "Рассчитать" ============================================

if __name__ == "__main__":

    try:
        all_prd = get_all_products(db_name, tbl1_name)
        all_usrs = get_all_products(db_name, tbl2_name)
    except:
        print(f'База данных{db_name} или таблицы {tbl1_name} и {tbl2_name} не существуют.')
        if input('Инициализироовать их ? (y/n)') == 'y':
            initiate_db(db_name, tbl1_name, tbl2_name)
        else:
            print('Сожалею. Но без инициализации БД работать нельзя.')
            print('Завершение работы')
            quit()

    if not all_prd:
        print('Список продуктов пуст.')
        print('Завершение работы.')
        quit()
    print(all_prd)
    print(all_usrs)
    executor.start_polling(dp, skip_updates=True)
