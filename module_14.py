import sqlite3

""" 
Изначально файл 'not_telegram.db' не создаем.
При создании подключения он будет создан автоматически.
"""
def print_users(users):
    for i in range(len(users)):
        print(f'Имя: {users[i][1]} | Почта: {users[i][2]} | Возраст: {users[i][3]} | Баланс: {users[i][4]}')

connection = sqlite3.connect('not_telegram.db')  # Создаем и подключаемся. Или подключаемся
cursor = connection.cursor()  # Создаем указатель на БД

# Создаем таблицу БД (Если она не существует)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER
)
''')
"""
Перед заполнением таблицы проверим, что она пустая.
Для этого проверим результат запроса SELECT *
"""
cursor.execute('SELECT * FROM Users')
users = cursor.fetchall()
if not users:
    # Заполняем таблицу данными
    for i in range(1, 11):
        cursor.execute('INSERT INTO Users(username, email, age, balance) VALUES(?, ?, ?, ?)',
                       (f'User{i}', f'example{i}@gmail.com', i*10, 1000)
                       )

# Выводим таблицу на печать
print('Все Users')
cursor.execute('SELECT * FROM Users')
users = cursor.fetchall()
print_users(users)

print('Обновляем баланс у каждого второго')
cursor.execute('UPDATE Users SET balance=?  WHERE (id-1) % 2 = 0', (500,))
cursor.execute('SELECT * FROM Users')
users = cursor.fetchall()
print_users(users)

print('Удаляем каждого третьего')
cursor.execute('DELETE FROM Users WHERE (id-1) % 3 = 0')
cursor.execute('SELECT * FROM Users')
users = cursor.fetchall()
print_users(users)

print('Выводим всех, кому не 60')
cursor.execute('SELECT * FROM Users WHERE age != 60')
users = cursor.fetchall()
print_users(users)

connection.commit()
cursor.close()
