""" клиентская часть """

import sys
import json
import time
import re
import logging
import logs.config_client_log
from lib.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, AUTH, ALERT, MSG, ERR200, ERR400, \
    CLIENT_LISTEN, LISTEN, SENDER, MSG, MSG_TEXT, ERROR
from lib.utils import create_socket, server_settings, get_message, send_message
from lib.errors import ReqFieldMissingError, ServerError
from logs.decoration_log import log

CLIENT_LOGGER = logging.getLogger('client')

@log
def message_from_server(message):
    """Функция - обработчик сообщений других пользователей, поступающих с сервера"""
    if ACTION in message and message[ACTION] == MSG and \
            SENDER in message and MSG_TEXT in message:
        print(f'Получено сообщение от пользователя {message[SENDER]}:\n{message[MSG_TEXT]}')
        CLIENT_LOGGER.info(f'Получено сообщение от пользователя {message[SENDER]}:\n{message[MSG_TEXT]}')
    else:
        CLIENT_LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')

@log
def create_message(sock, account_name='Guest'):
    """Функция запрашивает текст сообщения и возвращает его.
    Так же завершает работу при вводе подобной комманды
    """
    message = input('Введите сообщение для отправки или \'exit\' для завершения работы: ')
    if message.lower() == 'exit':
        sock.close()
        CLIENT_LOGGER.info('Завершение работы по команде пользователя.')
        sys.exit(0)
    message_dict = {ACTION: MSG,TIME: time.time(),ACCOUNT_NAME: account_name,MSG_TEXT: message}
    CLIENT_LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict

@log
def create_presence(account_name='Guest'):
    '''
    Функция генерирует запрос о присутствии клиента
    :param account_name:
    :return:
    '''
    # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
    out = {ACTION: PRESENCE, TIME: time.time(), USER: {ACCOUNT_NAME: account_name}}
    CLIENT_LOGGER.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out

@log
def get_user():
    """
    функция возвращает имя пользователя
    :return:
    """
    while True:
        account = input("введите имя пользователя >>>")
        if not re.match(r"[A-Za-z]", account) or len(account) > 25 or len(account) < 3:
            CLIENT_LOGGER.error(f"недопустимое имя пользователя: {account}")
            print("Имя пользователя должно быть от 3 до 25 латинских символов")
        elif account.lower().strip() == 'guest':
            CLIENT_LOGGER.error(f"недопустимое имя пользователя: {account}")
            print("Недоспустимое имя пользователя")
        else:
            break
    return account


@log
def create_action(account_name, action, msg=None):
    '''
    Функция отдает словарь с текстом сообщения
    :param account_name:
    :return:
    '''
    # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
    out = {ACTION: action, TIME: time.time(), USER: {ACCOUNT_NAME: account_name}, MSG: msg}
    CLIENT_LOGGER.debug(f'Сформировано {ACTION} сообщение для пользователя {account_name}')
    return out

@log
def process_handler(message):
    '''
    Функция разбирает ответ сервера
    :param message:
    :return:
    '''
    CLIENT_LOGGER.debug(f'Разбор приветственного сообщения от сервера: {message}')
    print(f'Разбор приветственного сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE]==200: #message[RESPONSE]==200:
            CLIENT_LOGGER.debug(f"{message[RESPONSE]} содержит {ERR200}")
            return message[MSG] #ERR200
        elif message[RESPONSE]==ERR400: #message[RESPONSE]==400:
            CLIENT_LOGGER.debug(f"{message[RESPONSE]} содержит {ERR400}")
            raise ServerError(f"{ERR400}: {message[ERROR]}")
    raise ReqFieldMissingError(RESPONSE)


@log
def start_client():
    srv_settings = server_settings()
    server_address = srv_settings[0]
    server_port = srv_settings[1]
    client_listen = srv_settings[2]

    print(f"start client on: {server_address}:{server_port} | listen_mode={client_listen}")
    CLIENT_LOGGER.info(f"client started {server_address}:{server_port} | listen_mode={client_listen}")

    try:
        transport = create_socket()
        transport.connect((server_address, server_port))
        send_message(transport, create_presence())
        answer = process_handler(get_message(transport))
        CLIENT_LOGGER.info(f"соединение с сервером {server_address}:{server_port}. Ответ: {answer}")
        print(f"соединение с сервером {server_address}:{server_port}. Ответ: {answer}")

# авторизация
        account_name = get_user()
        CLIENT_LOGGER.info(f"Guest авторизовался как {account_name}")
        CLIENT_LOGGER.debug(f"отправка {AUTH} сообщения на сервер {server_address}:{server_port} от user={account_name}")
        message_to_server = create_action(account_name, action=AUTH, msg=None)
        send_message(transport, message_to_server)
        try:
            answer = process_handler(get_message(transport))
            print(answer)
        except (ValueError, json.JSONDecodeError):
            print(answer)
            CLIENT_LOGGER.error(f"{ERR400}. Не удалось декодировать сообшение от сервера")
            print(f"{ERR400}. Не удалось декодировать сообшение от сервера")


    except json.JSONDecodeError:
        CLIENT_LOGGER.error(f"не удалось декодировать JSON-строку")
        print(f"не удалось декодировать JSON-строку")
        sys.exit(1)
    except ServerError as error:
        CLIENT_LOGGER.error(f"ошибка при установке соединения: {error.text}")
        print(f"ошибка при установке соединения: {error.text}")
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        CLIENT_LOGGER.error(f"в ответе сервера нет обязательного поля {missing_error.missing_field}")
        sys.exit(1)
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f"Не удалось подключиться к серверу {server_address}:{server_port}")
        sys.exit(1)
    else:
        print(f"клиент - в режиме client_listen={client_listen:}")
    while True:
        if not client_listen:
            try:
                send_message(transport, create_message(transport))
            except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                CLIENT_LOGGER.error(f"соединение с сервером {server_address}:{server_port} потеряно")
                print(f"соединение с сервером {server_address}:{server_port} потеряно")
                sys.exit(1)
        if client_listen:
            try:
                message_from_server(get_message(transport))
            except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                CLIENT_LOGGER.error(f"соединение с сервером {server_address}:{server_port} потеряно")
                print(f"соединение с сервером {server_address}:{server_port} потеряно")
                sys.exit(1)


if __name__ == '__main__':
    start_client()
