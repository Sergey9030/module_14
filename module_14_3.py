from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


api = "7894373187:AAG6EizTKiQDfLof5qLUszC9oeTyDhckb6k"
bot = Bot(token=api)  # Бот
dp = Dispatcher(bot, storage=MemoryStorage())  # Диспетчер

# Создаем клавиатуры.

# Основная клавиатура.
# Запускается при старте бота.
kb = ReplyKeyboardMarkup(resize_keyboard=True)  #  Создаем клавиатуру
bt_info = KeyboardButton(text='Информация')  # Создаем Кнопку1
bt_go = KeyboardButton(text='Рассчитать')  # Создаем Кнопку2
bt_buy = KeyboardButton(text='Купить')  # Создаем Кнопку3
kb.add(bt_go, bt_info)  # Добавили две кнопки в первый ряд
kb.add(bt_buy)  # И третью в следующий ряд

# Инлай клавиатура для расчета калорий.
# Запускается при нажатии кнопки "Рассчитать"
ikb = InlineKeyboardMarkup(resize_keyboard=True)  # Клавиатура для Рассчитать
ibt_info = InlineKeyboardButton(text='Формула расчета', callback_data='formulas')
ibt_go = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
ikb.add(ibt_go, ibt_info)

# Инлай клавиатура для покупок.
# Запускается при нажатии кнопки "Купить"
ikb_buy = InlineKeyboardMarkup(resize_keyboard=True)  # Клавиатура для Купить
ikb_p1 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
ikb_p2 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
ikb_p3 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
ikb_p4 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
ikb_buy.add(ikb_p1, ikb_p2, ikb_p3, ikb_p4)


class UserState(StatesGroup):
    name = State()      # Имя
    age = State()       # Возраст
    growth = State()    # Рост
    weight = State()    # Вес

# Реакция на команду "/start".
# Выводит приветствие и запускает основную клавиатуру.
@dp.message_handler(commands='start')
async def start(message):
    await message.answer('Здравствуйте.')
    await message.answer('Я бот, который расчитает для Вас необходимое количество калорий в сутки.', reply_markup=kb)
    await message.answer('Для начала расчета, получения информации или покупок воспользуйтесь кнопками внизу экрана.')

# Реакция на нажатие кнопки "Купить".
# Выводит название продукта, его фото, описание и цену.
# Заускает инлайн клавиатуру для покупок.
@dp.message_handler(text='Купить')
async def get_buying_list(message):
    with open('Product1.png', 'rb') as p1:
        await message.answer_photo(p1, 'Название: Product1 | Очищение кишечника | Цена: 634')
    with open('Product2.png', 'rb') as p2:
        await message.answer_photo(p2, 'Название: Product2 | Заменитель сахара | Цена: 165')
    with open('Product3.png', 'rb') as p3:
        await message.answer_photo(p3, 'Название: Product3 | Шелуха семян подорожника | Цена: 585')
    with open('Product4.png', 'rb') as p4:
        await message.answer_photo(p4, 'Название: Product4 | Шелуха семян подорожника по акции | Цена: 221')
    await message.answer('ыберите продукт для покупки:', reply_markup=ikb_buy)

# Реакция на нажатие любой из кнопок клавиатуры для покупок.
# Выводит сообщение об успешной покупке.
@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

# Реакция на на жатие кнопки "Рассчитать".
# Предлагает выбрать опцию и запускает инлайн клавиатуру для расчета калорий.
@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup=ikb)

# Реакция на на жатие кнопки "Информация".
# Выводит сообщение о боте.
@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Я бот, который расчитает для Вас необходимое количество калорий в сутки.')

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

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)