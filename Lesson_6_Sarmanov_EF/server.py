""" серверная часть """
import json
import logging
import logs.config_server_log
from lib.variables import MAX_CONNECTIONS, PRESENCE, ACTION, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, ALERT, AUTH, \
    MSG, ERR200, ERR400
from lib.utils import server_settings, create_socket, get_message, send_message
from logs.decoration_log import log

SERVER_LOGGER = logging.getLogger('server')


@log
def client_message_handler(message):
    '''
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клиента, проверяет корректность, возвращает словарь-ответ для клиента
    {ACTION: PRESENCE|AUTH|MSG, TIME: time.time(),USER: {ACCOUNT_NAME: account_name}, MSG:message_str}
    :param message:
    :return:
    '''
    SERVER_LOGGER.debug(f'функция разбора сообщения от клиента: {message}')
    if ACTION not in message or TIME not in message or USER not in message:
        SERVER_LOGGER.error(f'сообщение от клиента не содержит обязательного поля ACTION: {message}')
        return {RESPONSE: 400, ERROR: ERR400}
    elif message[ACTION] == PRESENCE:  # and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200, ERROR: ERR200, MSG:"Welcome, Гость"}
    elif message[ACTION] == AUTH and message[USER][ACCOUNT_NAME] != 'Guest':
        return {RESPONSE: 200, ERROR: ERR200, MSG:f"Welcome, {message[USER][ACCOUNT_NAME]}"}
    elif message[ACTION] == MSG and message[USER][ACCOUNT_NAME] != 'Guest':
        return {RESPONSE: 200, ERROR: ERR200, MSG:message[MSG]}
    return {RESPONSE: 400, ERROR: ERR400}

@log
def start_server():
    srv_settings = server_settings()
    server_address = srv_settings[0]
    server_port = srv_settings[1]
    transport = create_socket()
    transport.bind((server_address, server_port))
    transport.listen(MAX_CONNECTIONS)
    print(f"server start on: {server_address}:{server_port}")
    SERVER_LOGGER.info(f"server started on {server_address}:{server_port}")

    while True:
        client, client_address = transport.accept()
        SERVER_LOGGER.debug(f'client | {client_address}')
        try:
            message_from_client = get_message(client)
            SERVER_LOGGER.info(f"client_message:{client_address} | {message_from_client}")
            #print("message_from_client:", message_from_client)
            # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
            response = client_message_handler(message_from_client)
            send_message(client, response)
            SERVER_LOGGER.info(f"send_message {client_address} | {response}")
            # client.close()
        except (ValueError, json.JSONDecodeError):
            SERVER_LOGGER.error(f'Принято некорретное сообщение от клиента: {client_address}')
            #print('Принято некорретное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    start_server()
