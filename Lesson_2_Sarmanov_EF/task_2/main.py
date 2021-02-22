"""
2. Задание на закрепление знаний по модулю json. Есть файл orders
в формате JSON с информацией о заказах. Написать скрипт, автоматизирующий
его заполнение данными.

Для этого:
Создать функцию write_order_to_json(), в которую передается
5 параметров — товар (item), количество (quantity), цена (price),
покупатель (buyer), дата (date). Функция должна предусматривать запись
данных в виде словаря в файл orders.json. При записи данных указать
величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json()
с передачей в нее значений каждого параметра.

ПРОШУ ВАС НЕ УДАЛЯТЬ ИСХОДНЫЙ JSON-ФАЙЛ
ПРИМЕР ТОГО, ЧТО ДОЛЖНО ПОЛУЧИТЬСЯ

{
    "orders": [
        {
            "item": "printer",
            "quantity": "10",
            "price": "6700",
            "buyer": "Ivanov I.I.",
            "date": "24.09.2017"
        },
        {
            "item": "scaner",
            "quantity": "20",
            "price": "10000",
            "buyer": "Petrov P.P.",
            "date": "11.01.2018"
        }
    ]
}

вам нужно подгрузить JSON-объект
и достучаться до списка, который и нужно пополнять
а потом сохранять все в файл
"""
import json


def write_order_to_json(v_item, v_quantity, v_price, v_buyer, v_date):
    w_file = "test.json"  # файл для записи json
    value_lst = orders.get("orders")  # вытащим из словаря список-значение и добавим в него новые данные
    value_lst.append({"item": v_item, "quantity": v_quantity, "price": v_price, "buyer": v_buyer, "date": v_date})
    orders["orders"] = value_lst
    with open(w_file, 'w') as obj_file:  # запишем обновленный словарь в виде json в файл
        json.dump(orders, obj_file, sort_keys=False, indent=4)


def fill_data():
    for tmp_dic in example_data:
        tmp_item = tmp_dic.get(headers[0])
        tmp_quantity = tmp_dic.get(headers[1])
        tmp_price = tmp_dic.get(headers[2])
        tmp_buyer = tmp_dic.get(headers[3])
        tmp_date = tmp_dic.get(headers[4])
        write_order_to_json(tmp_item, tmp_quantity, tmp_price, tmp_buyer, tmp_date)


orders = {"orders": []}  # словарь для наполнения и выгрузки в json
headers = ["item", "quantity", "price", "buyer", "date"]  # заголовки, для быстрого редактирования

# пример данных для заполнения
example_data = [
    {headers[0]: "printer", headers[1]: "10", headers[2]: "6700", headers[3]: "Ivanov I.I.", headers[4]: "24.09.2017"},
    {headers[0]: "scaner", headers[1]: "20", headers[2]: "10000", headers[3]: "Petrov P.P.", headers[4]: "11.01.2018"},
    {headers[0]: "computer", headers[1]: "5", headers[2]: "40000", headers[3]: "Sidorov S.S.", headers[4]: "2.05.2019"},
    {headers[0]: "printer", headers[1]: "10", headers[2]: "6700", headers[3]: "Ivanov I.I.", headers[4]: "24.09.2017"},
    {headers[0]: "scaner", headers[1]: "20", headers[2]: "10000", headers[3]: "Petrov P.P.", headers[4]: "11.01.2018"},
    {headers[0]: "computer", headers[1]: "5", headers[2]: "40000", headers[3]: "Sidorov S.S.", headers[4]: "2.05.2019"}
]
print("выгрузка данных в test.json ...")
fill_data()
print("готово")
