import sqlite3

def print_users(users):
    for i in range(len(users)):
        print(f'Имя: {users[i][1]} | Почта: {users[i][2]} | Возраст: {users[i][3]} | Баланс: {users[i][4]}')


connection = sqlite3.connect('not_telegram.db')  # Создаем и подключаемся. Или подключаемся
cursor = connection.cursor()  # Создаем указатель на БД


cursor.execute('SELECT * FROM Users')
users = cursor.fetchall()
print('Все Users')
print_users(users)

cursor.execute('DELETE FROM Users WHERE id=6;')
print('Удалили №6')
cursor.execute('SELECT * FROM Users')
users = cursor.fetchall()
print_users(users)

cursor.execute('SELECT Count(id) FROM Users;')
total_users = cursor.fetchall()[0][0]
print('Всего пользователей: ', total_users)

cursor.execute('SELECT Sum(balance) FROM Users;')
all_balances = cursor.fetchall()[0][0]
print('Общий баланс: ', all_balances)

cursor.execute('SELECT Avg(balance) FROM Users;')
avg_balance = cursor.fetchall()[0][0]
print('Средний баланс: ', avg_balance, '| all_balances/total_users=', all_balances/total_users)

# connection.commit()  Транзакцию не проводим (Удаление №6 не сохраниться).
connection.close()
