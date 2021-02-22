"""
3. Задание на закрепление знаний по модулю yaml.
 Написать скрипт, автоматизирующий сохранение данных
 в файле YAML-формата.
Для этого:

Подготовить данные для записи в виде словаря, в котором
первому ключу соответствует список, второму — целое число,
третьему — вложенный словарь, где значение каждого ключа —
это целое число с юникод-символом, отсутствующим в кодировке
ASCII(например, €);

Реализовать сохранение данных в файл формата YAML — например,
в файл file.yaml. При этом обеспечить стилизацию файла с помощью
параметра default_flow_style, а также установить возможность работы
с юникодом: allow_unicode = True;

Реализовать считывание данных из созданного файла и проверить,
совпадают ли они с исходными.
"""
import yaml


def write_yaml(data_to_yaml):
    with open('test.yaml', mode='w', encoding='utf-8') as f_obj:
        yaml.dump(data_to_yaml, f_obj, default_flow_style=False, allow_unicode=True)


def open_yaml():
    with open('test.yaml', mode='r', encoding='utf-8') as f_obj:
        f_obj_content = yaml.safe_load(f_obj)
    return f_obj_content


currency = chr(163)
items = ["computer", "printer", "keyboard", "mouse"]
items_quantity = len(items)
items_price = {"computer": str(200) + currency, "keyboard": str(5) + currency, "mouse": str(4) + currency
    , "printer": str(100) + currency
               }

example_data = {"items": items, "items_quantity": items_quantity, "items_price": items_price}

print("экспорт example_data в yaml ...")
write_yaml(example_data)
print("готово.")

print()
print("импорт yaml в python объект")
yaml_data = open_yaml()
print("импорт завершен")
print()

print("исходный объект, экспортированный в yaml:")
print(example_data)
print("импортированный yaml в объект:")
print(yaml_data)

#write_yaml(yaml_data)