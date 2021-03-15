""" серверная часть """
import json
import logging
import select
import time
import sys
import logs.config_server_log
from lib.variables import MAX_CONNECTIONS, PRESENCE, ACTION, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, ALERT, AUTH, \
    MSG, ERR200, ERR400, SERVER_TIMEOUT, ENCODING, PACKAGE_LENGTH, LISTEN, SENDER, MSG_TEXT
from lib.utils import server_settings, create_socket, get_message, send_message
from logs.decoration_log import log

SERVER_LOGGER = logging.getLogger('server')


@log
def client_message_handler(message, messages_list, client):
    '''
    Обработчик сообщений от клиентов, принимает словарь - сообщение от клинта,
    проверяет корректность, отправляет словарь-ответ для клиента с результатом приёма.
    :param message:
    :param messages_list:
    :param client:
    :return:
    '''
    SERVER_LOGGER.info(f'функция разбора message от клиента: {message}')
    if ACTION not in message:
        SERVER_LOGGER.error(f"сообщение от клиента не содержит обязательного поля ACTION: {message}")
        print(f"сообщение от клиента не содержит обязательного поля ACTION: {message}")
        send_message(client, {RESPONSE: 400, ERROR: ERR400})
    elif TIME not in message:
        SERVER_LOGGER.error(f"сообщение от клиента не содержит обязательного поля TIME: {message}")
        print(f"сообщение от клиента не содержит обязательного поля TIME: {message}")
        send_message(client, {RESPONSE: 400, ERROR: ERR400})
    elif ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message and message[USER][
        ACCOUNT_NAME] == 'Guest':
        SERVER_LOGGER.debug(f"сформировано PRESENCE сообщение:{message}")
        print(f"сформировано PRESENCE сообщение:{message}")
        send_message(client, {RESPONSE: 200, ERROR: ERR200, MSG: str(f"Welcome, {message[USER][ACCOUNT_NAME]}")})
        return
    elif ACTION in message and message[ACTION] == AUTH and message[USER][ACCOUNT_NAME] != 'Guest':
        SERVER_LOGGER.debug(f"сформировано AUTH сообщение: {message}")
        print(f"сформировано AUTH сообщение:{message}")
        send_message(client, {RESPONSE: 200, ERROR: ERR200, MSG: str(f"Welcome, {message[USER][ACCOUNT_NAME]}")})
        # {RESPONSE: 200, ERROR: ERR200, MSG: f"Welcome, {message[USER][ACCOUNT_NAME]}"}
        return
    elif ACTION in message and message[ACTION] == MSG and TIME in message and MSG_TEXT in message:
        SERVER_LOGGER.debug(f"сформировано MSG сообщение: {message}")
        print(f"сформировано MSG сообщение:{message}")
        messages_list.append((message[ACCOUNT_NAME], message[MSG_TEXT]))
        return
    else:
        SERVER_LOGGER.error(f"функция разбора message от клиента, ни одно из условий не подошло: {message}")
        send_message(client, {RESPONSE: 400, ERROR: ERR400})
        return


@log
def start_server():
    srv_settings = server_settings()
    server_address = srv_settings[0]
    server_port = srv_settings[1]

    transport = create_socket()
    transport.bind((server_address, server_port))
    transport.settimeout(SERVER_TIMEOUT)
    transport.listen(MAX_CONNECTIONS)

    print(f"server start on: {server_address}:{server_port}")
    SERVER_LOGGER.info(f"server started on {server_address}:{server_port}")

    clients = []  # список клиентов
    messages = []  # список сообщений

    while True:
        try:
            client, client_address = transport.accept()
            SERVER_LOGGER.debug(f'client | {client_address}')
        except OSError:
            pass
        else:
            print(f"Получен запрос на соединение от {str(client_address)}")
            SERVER_LOGGER.info(f"установлено соедниение с клиентом {client_address}")
            clients.append(client)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []

        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    client_message_handler(get_message(client_with_message), messages, client_with_message)
                except:
                    SERVER_LOGGER.info(f"клиент {client_with_message.getpeername()} отключился")
                    print(f"клиент {client_with_message.getpeername()} отключился")
                    clients.remove(client_with_message)

        if messages and send_data_lst:
            message = {ACTION: MSG, SENDER: messages[0][0], TIME: time.time(), MSG_TEXT: messages[0][1]}
            SERVER_LOGGER.debug(f"message in send_data_list {message}")
            print(message)
            del messages[0]
            for waiting_client in send_data_lst:
                try:
                    SERVER_LOGGER.debug(f"send message: {message} to client: {waiting_client}")
                    print(f"send message: {message} to client: {waiting_client}")
                    send_message(waiting_client, message)
                except:
                    SERVER_LOGGER.info(f"клиент {client_with_message.getpeername()} отключился")
                    print(f"клиент {client_with_message.getpeername()} отключился")
                    clients.remove(waiting_client)


if __name__ == '__main__':
    start_server()
