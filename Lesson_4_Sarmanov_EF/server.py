""" серверная часть """
import json

from lib.variables import MAX_CONNECTIONS, PRESENCE, ACTION, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, ALERT, AUTH, \
    MSG, ERR200, ERR400
from lib.utils import server_settings, create_socket, get_message, send_message


def client_message_handler(message):
    '''
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клиента, проверяет корректность, возвращает словарь-ответ для клиента
    {ACTION: PRESENCE|AUTH|MSG, TIME: time.time(),USER: {ACCOUNT_NAME: account_name}, MSG:message_str}
    :param message:
    :return:
    '''
    if ACTION not in message or TIME not in message or USER not in message:
        return {RESPONSE: 400, ERROR: ERR400}
    elif message[ACTION] == PRESENCE:  # and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200, ERROR: ERR200, MSG:"Welcome, Гость"}
    elif message[ACTION] == AUTH and message[USER][ACCOUNT_NAME] != 'Guest':
        return {RESPONSE: 200, ERROR: ERR200, MSG:f"Welcome, {message[USER][ACCOUNT_NAME]}"}
    elif message[ACTION] == MSG and message[USER][ACCOUNT_NAME] != 'Guest':
        return {RESPONSE: 200, ERROR: ERR200, MSG:message[MSG]}
    return {RESPONSE: 400, ERROR: ERR400}


def start_server():
    srv_settings = server_settings()
    server_address = srv_settings[0]
    server_port = srv_settings[1]
    print(f"server start on: {server_address}:{server_port}")
    transport = create_socket()
    transport.bind((server_address, server_port))
    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        try:
            message_from_client = get_message(client)
            print("message_from_client:", message_from_client)
            # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
            response = client_message_handler(message_from_client)
            send_message(client, response)
            # client.close()
        except (ValueError, json.JSONDecodeError):
            print('Принято некорретное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    start_server()
