"""
Задание 5.

Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.

Подсказки:
--- используйте модуль chardet, иначе задание не засчитается!!!
"""
import subprocess
import chardet


def print_res(ARGS):
    res_bytes = subprocess.check_output(ARGS)
    code_dic = chardet.detect(res_bytes)
    print()
    print(f"======================== {ARGS[1].upper()} ========================")
    print()
    print("-------------- декодирование из кодов примеров --------------", end='')
    res_str = res_bytes.decode(code_dic['encoding']).encode('utf-8')
    print(res_str.decode('utf-8'), end='')
    print()
    print("-------------- декодирование без перевода в utf --------------", end='')
    res_str = res_bytes.decode(code_dic['encoding'])
    print(res_str, end='')
    return


print_res(['ping', 'yandex.ru'])
print_res(['ping', 'youtube.com'])
