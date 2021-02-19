"""
Задание 6.

Создать  НЕ программно (вручную) текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор».

Принудительно программно открыть файл в формате Unicode и вывести его содержимое.
Что это значит? Это значит, что при чтении файла вы должны явно указать кодировку utf-8
и файл должен открыться у ЛЮБОГО!!! человека при запуске вашего скрипта.

При сдаче задания в папке должен лежать текстовый файл!

Это значит вы должны предусмотреть случай, что вы по дефолту записали файл в cp1251,
а прочитать пытаетесь в utf-8.

Преподаватель будет запускать ваш скрипт и ошибок НЕ ДОЛЖНО появиться!

Подсказки:
--- обратите внимание, что заполнять файл вы можете в любой кодировке
но открыть нужно ИМЕННО!!! в формате Unicode (utf-8)
--- обратите внимание на чтение файла в режиме rb
для последующей переконвертации в нужную кодировку

НАРУШЕНИЕ обозначенных условий - задание не выполнено!!!
"""
import chardet

c_file = "test_file.txt"
c_file2 = "test_file2.txt"

with open(c_file, mode="rb") as w_file:
    for line in w_file:
        code_dic = chardet.detect(line)
        row_str = line.decode(code_dic['encoding']).encode('utf-8')
        decode_str = row_str.decode('utf-8')
        print(f"{decode_str}", end='')

print()
print("-------------------------- пример преподавателя --------------------------")
def encod_convert():
    with open(c_file2, mode='rb') as f_obj:
        content_byte=f_obj.read()
    detected=chardet.detect(content_byte)
    encoding=detected[('encoding')]
    content_text=content_byte.decode(encoding)
    with open(c_file2, 'w', encoding='utf=8') as f_obj:
        f_obj.write(content_text)

encod_convert()

with open(c_file2, 'r', encoding='utf-8') as file:
    content=file.read()
print(content)
