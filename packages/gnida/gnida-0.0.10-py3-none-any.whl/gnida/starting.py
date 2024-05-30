menu = [
    '3.Дан список А3, состоящий из четного количества элементов. Используя функцию (функции) высшего порядка разбейте его на списки В, С так, чтобы в одном были положительные элементы, а в другом отрицательные.',
    '6.Создать класс стек. Использовать способ реализации стека через list. Удалить каждый второй элемент стека.',
    '9. Дан список S состоящий из N различных элементов. Вывести индексы четных элементов списка. Использовать встроенные функции высшего порядка'
]

content = ''


def console_menu():
    return '\n'.join(menu)


def read_code(name):
    global content
    with open(f'./c/{name}.py', 'r', encoding='utf-8') as file:
        content = file.read()
    return content


def write_me(name):
    global content
    with open(f"{name}.py", "w+") as my_file:
        my_file.write(content)
    return 'Все получилось'
