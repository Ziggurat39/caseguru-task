import psycopg2
from psycopg2 import Error


task = 2


# Пробуем подключиться к БД и выполнить запрос.
try:
    # Определяем конфигурацию соединения.
    connection = psycopg2.connect(user='trainee_user',
                        password='trainee_pass',
                        host='nodus.caseguru.ru',
                        port='5432',
                        dbname='testtask')

    print('Соединение с сервером установлено.')

    cursor = connection.cursor()
    
    # Отправляем запрос.
    cursor.execute('''SELECT orders.managerid AS Manager, AVG(orders.processing_time) AS Time
                   FROM orders
                   INNER JOIN statuses ON orders.statuscode = statuses.code
                   WHERE statuses.status_group='Выполнен' AND orders.createdat BETWEEN '2022/06/01 00:00:00' AND '2022/08/31 23:59:59.993'
                   GROUP BY orders.managerid
                   ORDER BY orders.managerid DESC;''')
    # Получаем все подходящие результаты.
    fetch = cursor.fetchall()
    
    # Чистим получившийся лист от Decimal. Элементы листа - кортежи, неизменяемы, создаем новый лист.
    fixed_fetch = []
    for row in fetch:
        fixed_fetch.append(list(map(str, list(row))))
    
    max = 0
    id = None
    
    # Ищем самого долгого менеджера, результат записывем в payload.
    for i in range(len(fixed_fetch)):
        element = round(float(fixed_fetch[i][1]))
        if max < element:
            max = element
            id = fixed_fetch[i][0]
    
    payload = str(id) + str(max)

# Ловим возможные ошибки.
except (Exception, Error) as error:
    print(error)
    print('Что-то пошло не так и все упало...')

# Закрываем курсор и соединение.
finally:
    if connection:
        cursor.close()
        connection.close()
        print('Соединение с сервером закрыто.')
