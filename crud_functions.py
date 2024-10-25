"""
add_data(db_name, tlb_name)
    Добавляет данные в таблицу <tlb_name> находящуюся в базе данных <db_name>.

initiate_db(db_name, tlb_name):
    # Подключается к <db_name> и таблице <tlb_name>
    # Если <tlb_name> пуста предлагает заполнить ее.

def get_all_products(db_name, tlb_name):
    # Выводит содержимое таблицы <tlb_name>, находящуюся в базе данных <db_name>.

"""
import sqlite3

def isdigit(s):
# Проверка, что строка является числовым значением
    try:
        float(s)
        return True
    except:
        return False
def add_data(db_name, tbl_name):
# Добавляет данные в таблицу <tbl_name> находящуюся в базе данных <db_name>.
    connection = sqlite3.connect(db_name)  # Создаем соединение
    cursor = connection.cursor()

    # Получаем данные от пользователя
    print(f'Добавляем данные в таблицу {db_name}/{tbl_name}.')
    go = 'y'
    while go == 'y':
        title = ''
        description = ''
        price = ''
        picture = ''

        title = input('Введите название продукта: ')
        while title == '':
            print('Название продукта не может быть пустым.')
            title = input('Введите название продукта: ')

        description = input('Введите описание продукта: ')

        price = input('Введите цену продукта: ')
        while not isdigit(price):
            print('Неверное значение для цены.')
            price = input('Введите цену продукта: ')

        picture = input('Введите название файла картинки: ')

        # Проверяем возможност выполнения запроса
        try:
            # Добавляем данные в таблицу с помощью запроса
            cursor.execute(f"INSERT INTO {tbl_name}( title, description, price, picture ) "
                                f"SELECT '{title}', '{description}', {price}, '{picture}';")
                                # SQL любит получать данные из запроса.
            print(f'Данные: Название="{title}", Описание="{description}", Цена="{price}", Изображение="{picture}"')
            print('Успешно добавлены.')
            connection.commit()  # Проводим транзакцию
        except sqlite3.IntegrityError:
            print(f'Нарушена уникальность наименования "{title}". Данные не добавлены.')

        go = input('Продлжим? (y/n)')
    connection.commit()
    cursor.close()  # Закрываем соединение


def initiate_db(db_name, tbl_name):
# Подключается к <db_name> и таблице <tbl_name>
# Если <tbl_name> пуста предлагает заполнить ее.

    # Создаем подключение
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    # Создаем таблицу, если ее нет.
    cursor.execute(f'CREATE TABLE IF NOT EXISTS {tbl_name}'
                                                f'(id INTEGER PRIMARY KEY, '
                                                f'title TEXT UNIQUE NOT NULL, '
                                                f'description TEXT, '
                                                f'price INTEGER NOT NULL, '
                                                f'picture TEXT)')

    # Если таблица пуста предлагаем ее заполнить.
    if not cursor.execute(f'SELECT * FROM {tbl_name}').fetchall():
        print(f'Таблица "{tbl_name}" пуста.')
        if input('Будем ее заполнять? (y/n)') == 'y':
            add_data(db_name, tbl_name)
        else:
            print('А зря...')
    connection.commit()
    cursor.close()

def get_all_products(db_name, tbl_name):
# Возврфщает содержимое таблицы <tbl_name>
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM {tbl_name}')
    all_tbl = cursor.fetchall()
    connection.close()
    return all_tbl

if __name__ == '__main__':

    initiate_db('TestDB.db', 'TestTbl')

    products = get_all_products('TestDB.db', 'TestTbl')
    for i in range(len(products)):
        print(products[i])
