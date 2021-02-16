"""
Задание 4.

Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
"""
v_lst = ["разработка", "администрирование", "protocol", "standard"]
v_lst_byte = []
code_standart = 'utf-8'

for el in v_lst:
    el_byte = el.encode(code_standart)
    print(f": {el}  {type(el)} | {el_byte}  {type(el_byte)}")
    v_lst_byte.append(el_byte)

print("-" * 80)

for el in v_lst_byte:
    el_str = el.decode(code_standart)
    print(f": {el}  {type(el)} | {el_str}  {type(el_str)}")
