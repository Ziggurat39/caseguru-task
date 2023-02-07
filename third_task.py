import re


# Разбиваем на токены с помощью регулярки, отбрасываем пустые строки.
def tokenize(s):
    return filter(None, _tokenizer(s))


# Итерация по токенам и построение вложенных списков на месте скобок с помощью стека.
def parse_conditions(expr):
    stack = []
    items = []
    for token in tokenize(expr):
        if token == '{':
            stack.append(items)
            items.append([])
            items = items[-1]
        elif token == '}':
            if not stack:
                raise ValueError("Несбалансированные скобки")
            items = stack.pop()
        else:
            items.append(token)
    if stack:
        raise ValueError("Несбалансированные скобки")
    return items


# Идем по полученному списку, строим строку рекурсивно.
def convert_to_string(initial_list):
    temp_string = ""
    for i, obj in enumerate(initial_list[:-1]):
        if type(initial_list[i+1]) is str and type(obj) is str:
            temp_string += obj
        elif type(initial_list[i+1]) is list:
            if len(initial_list[i+1]) == 1:
                temp_string += int(obj) * initial_list[i+1][0]
            else:
                temp_string += int(obj) * convert_to_string(initial_list[i+1])

    return temp_string

# Определяем переменные для работы.
task = 3
payload = ''
input_data = "ab2{g}3{a2{fg}}"

_tokenizer = re.compile(r'\s*(\d*)([{}])\s*').split
processed_data = convert_to_string(parse_conditions(input_data))
if processed_data == "":
    payload = input_data
else:
    payload = processed_data
