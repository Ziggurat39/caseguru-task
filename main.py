import requests
import re
from first_task import task as task1, payload as payload1
from second_task import task as task2, payload as payload2
from third_task import task as task3, payload as payload3


# Проверяем задачки, task - номер задания, result - ответ на него.
def check_task(task: int, result: str):
    url = 'https://nodus.caseguru.ru/trainee/tasks'
    payload = {'task': task, 'result': result}
    
    response = requests.post(url, json=payload)
    
    return response.json()['key']


# Формируем ключ из полученных частей.
def get_key():
    solution = []
    solution.append(check_task(task1, payload1))
    solution.append(check_task(task2, payload2))
    solution.append(check_task(task3, payload3))
    
    print(*solution, sep='-')

get_key()
