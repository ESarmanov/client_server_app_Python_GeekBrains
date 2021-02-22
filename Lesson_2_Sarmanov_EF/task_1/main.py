"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт,
осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt,
info_3.txt и формирующий новый «отчетный» файл в формате CSV.

Для этого:

Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
с данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно
получиться четыре списка — например, os_prod_list, os_name_list,
os_code_list, os_type_list. В этой же функции создать главный список
для хранения данных отчета — например, main_data — и поместить в него
названия столбцов отчета в виде списка: «Изготовитель системы»,
«Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data
(также для каждого файла);

Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;

Пример того, что должно получиться:

Изготовитель системы,Название ОС,Код продукта,Тип системы

1,LENOVO,Windows 7,00971-OEM-1982661-00231,x64-based

2,ACER,Windows 10,00971-OEM-1982661-00231,x64-based

3,DELL,Windows 8.1,00971-OEM-1982661-00231,x86-based

Обязательно проверьте, что у вас получается примерно то же самое.

ПРОШУ ВАС НЕ УДАЛЯТЬ СЛУЖЕБНЫЕ ФАЙЛЫ TXT И ИТОГОВЫЙ ФАЙЛ CSV!!!
"""

import csv
import re
import glob


def get_data(work_file):
    with open(work_file, mode='r') as w_file:
        tmp_dic = listname_dic.copy()
        for line in w_file:
            re_str = re.split(r': *', line)
            for head_el in header_list:
                if re_str[0].upper() == head_el.upper():
                    tmp_detail = listname_dic.get(head_el).lower()
                    # создадим детализованные файлы куда положим перечень найденных значений
                    with open(tmp_detail, mode='a') as tmp_detail_file:
                        tmp_detail_file.write(re_str[1])
                    # внесем в tmp словарь пару и обрежем перенос
                    tmp_dic[head_el] = re.sub(r' *\n$', '', str(re_str[1]))
        tmp_lst = []
        for el in tmp_dic.values():
            tmp_lst.append(el)
        main_data.append(tuple(tmp_lst))


def write_to_csv(w_file):
    file_list = glob.glob('info*.txt')  # все файлы по которым ищем
    for r_file in file_list:
        print(f"{chr(13)} ищу данные в файле {r_file}...")
        get_data(r_file)
    print(f"Начинаем экспорт...")
    with open(w_file, mode='w', newline='', encoding='utf=8') as f_obj:
        f_obj_write = csv.writer(f_obj)
        for row in main_data:
            f_obj_write.writerow(row)
    print(f"Экспорт завершен.")


def create_detail_file():
    for el in listname_dic.values():
        with open(str(el), mode='w', encoding='utf=8') as tmp_detail_file:
            pass


listname_dic = {"Изготовитель системы": "os_prod_list"
    , "Название ОС": "os_name_list"
    , "Код продукта": "os_code_list"
    , "Тип системы": "os_type_list"
                }

header_list = listname_dic.keys()
main_data = []  # основной список для экспорта
main_data.append(tuple(header_list))

create_detail_file()  # создадим пустые файлы для добавления в них информации

# экспорт main_data в csv
data_report_file = "main_data_report.csv"
print(f"Начинаем обработку...")
write_to_csv(data_report_file)
print(f"Обработка завершена...")
