""" Константы используемые в файлах проекта"""
import logging

DEFAULT_PORT = 7777       # порт по умолчанию
DEFAULT_IP = '127.0.0.1'  # IP адрес по умолчанию
MAX_CONNECTIONS = 5       # максимальная очередь подключений
PACKAGE_LENGTH = 1024     # длина сообщения в байтах
ENCODING = 'utf-8'        # кодировка

# Протокол JIM основные ключи:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'

# Прочие ключи, используемые в протоколе
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
AUTH='authenticate'
ALERT='alert'
MSG='msg'

ERR200='200:OK'
ERR400='400:Bad request'

# настройка логирования
LOG_LEVEL = logging.DEBUG
#LOG_LEVEL = logging.INFO
LOG_FORMATTER='%(asctime)s %(levelname)s %(filename)s %(message)s'
