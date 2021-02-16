"""
Задание 2.

Каждое из слов «class», «function», «method» записать в байтовом формате
без преобразования в последовательность кодов
не используя!!! методы encode и decode)
и определить тип, содержимое и длину соответствующих переменных.

Подсказки:
--- b'class' - используйте маркировку b''
--- используйте списки и циклы, не дублируйте функции
"""
from ast import literal_eval

v_lst = ["class", "function", "method"]

for i in range(len(v_lst)):
    byte_str = literal_eval("b'" + v_lst[i] + "'")
    print(f" буквеннный формат: {v_lst[i]} | тип: {type(v_lst[i])} | длина элемента: {len(v_lst[i])}")
    print(f" байтовый формат  : {byte_str} | тип: {type(byte_str)} | длина элемента: {len(byte_str)}")
    print("-" * 80)
