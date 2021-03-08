""" клиентская часть """

import json
import time
import re
import logging
import logs.config_client_log
from lib.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, AUTH, ALERT, MSG, ERR200, ERR400
from lib.utils import create_socket, server_settings,get_message, send_message

CLIENT_LOGGER = logging.getLogger('client')

def get_user():
    """
    функция возвращает имя пользователя
    :return:
    """
    while True:
        account = input("введите имя пользователя >>>")
        if not re.match(r"[A-Za-z]", account) or len(account)>25 or len(account)<3:
            CLIENT_LOGGER.error(f"недопустимое имя пользователя: {account}")
            print("Имя пользователя должно быть от 3 до 25 латинских символов")
        elif account.lower().strip()=='guest':
            CLIENT_LOGGER.error(f"недопустимое имя пользователя: {account}")
            print("Недоспустимое имя пользователя")
        else:
            break
    return account

def create_presence(account_name='Guest'):
    '''
    Функция генерирует запрос о присутствии клиента
    :param account_name:
    :return:
    '''
    # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
    out = {ACTION: PRESENCE,TIME: time.time(), USER: {ACCOUNT_NAME: account_name}}
    CLIENT_LOGGER.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out

def create_action(account_name, action, msg=None):
    '''
    Функция отдает словарь с текстом сообщения
    :param account_name:
    :return:
    '''
    # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
    out = {ACTION: action,TIME: time.time(), USER: {ACCOUNT_NAME: account_name}, MSG:msg}
    CLIENT_LOGGER.debug(f'Сформировано {ACTION} сообщение для пользователя {account_name}')
    return out


def process_handler(message):
    '''
    Функция разбирает ответ сервера
    :param message:
    :return:
    '''
    if RESPONSE not in message:
        CLIENT_LOGGER.error(f"{ERR400}: нет обязательного ключа {RESPONSE} в сообщении")
        return ERR400
    elif message[RESPONSE] == 200:
        return f"{message[MSG]}"
    raise ValueError

def transport_send(server_address, server_port, msg=None, account_name='Guest', action=AUTH):
    transport=create_socket()
    transport.connect((server_address, server_port))
    if account_name=='Guest':
        CLIENT_LOGGER.debug(f"{PRESENCE} to {account_name}")
        message_to_server = create_presence(account_name)
    else:
        message_to_server = create_action(account_name, action, msg)
        CLIENT_LOGGER.debug(f"send {message_to_server}")
    send_message(transport, message_to_server)
    try:
        answer = process_handler(get_message(transport))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        CLIENT_LOGGER.error(f"{ERR400}. Не удалось декодировать сообшение от сервера")
        print(f"{ERR400}. Не удалось декодировать сообшение от сервера")

def start_client():
    srv_settings=server_settings()
    server_address=srv_settings[0]
    server_port=srv_settings[1]
    print(f"start client on: {server_address}:{server_port}")
    CLIENT_LOGGER.info(f"client started {server_address}:{server_port}")
    transport_send(server_address, server_port)
    account_name = get_user()
    CLIENT_LOGGER.info(f"Guest авторизовался как {account_name}")
    CLIENT_LOGGER.debug(f"отправка {AUTH} сообщения на сервер {server_address}:{server_port} от user={account_name}")
    transport_send(server_address, server_port, account_name=account_name, action=AUTH)
    while True:
        msg=input(">")
        CLIENT_LOGGER.info(f"отправка сообщения {MSG}:{msg} на сервер {server_address}:{server_port} от user={account_name}")
        transport_send(server_address, server_port, account_name=account_name, action=MSG, msg=msg)


if __name__ == '__main__':
    start_client()
