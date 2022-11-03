import json
from dataclasses import dataclass

from pathlib import Path


@dataclass
class SmtpConfig:
    host: str = 'host:port'
    user_password: tuple = ('user', 'password')
    from_addr: str = 'from@from_host'
    to_addr: str = 'to@to_host'
    subject: str = 'WARNING Prom data update has falled'


# Read the start path
PATH_PROM = Path(__file__).parent

# To compile .exe file
# PATH_PROM = Path.cwd()

# Test base setting
PATH_BASE_TEST = Path("../tests/dbf/")

# For skipping tests that hit the real API server.
SKIP_REAL = False
# ON/OFF debug mode logging
DEBUG_MODE = True

#
SMTP_CONFIG = SmtpConfig()

if SKIP_REAL:
    HOST = 'my.prom.ua'
    AUTH_TOKEN_PRODUCTS = 'X'
    PATH_BASE = PATH_BASE_TEST
    LAST_PRODUCT_ID = 1616486427
else:
    config_prom_txt = PATH_PROM / 'config_prom.txt'
    with config_prom_txt.open() as f:
        config_prom_json = f.read()
        config_prom = json.loads(config_prom_json)

    # API Settigs
    HOST = config_prom['HOST']
    AUTH_TOKEN_PRODUCTS = config_prom['AUTH_TOKEN_PRODUCTS']

    # Base path setting
    PATH_BASE = Path(config_prom['PATH_BASE'])

    # ID на Prom последнего продукта.
    # Обновить при добавлении продуктов в каталог!
    LAST_PRODUCT_ID = config_prom['LAST_PRODUCT_ID']

    #
    SMTP_CONFIG.host = config_prom['SMTP_HOST']
    SMTP_CONFIG.user_password = tuple(config_prom['SMTP_USER_PASSWORD'])
    SMTP_CONFIG.from_addr = config_prom['SMTP_FROM_ADDR']
    SMTP_CONFIG.to_addr = config_prom['SMTP_TO_ADDR']

# Logging configuration by dictConfig
_format_console = '[%(filename)s-%(funcName)s].%(levelname)s: %(message)s'
_format_file = '%(asctime)s [%(filename)s-%(funcName)s].%(levelname)s: %(message)s'
LOGGING = {'version': 1,
           'formatters': {'formatter_0': {'datefmt': '%d/%m/%Y %H:%M:%S',
                                          'format': _format_console
                                          },
                          'formatter_1': {'datefmt': '%d/%m/%Y %H:%M:%S',
                                          'format': _format_file
                                          }
                          },
           'handlers': {'to_console': {'class': 'logging.StreamHandler',
                                       'formatter': 'formatter_0',
                                       'level': 'INFO'},
                        'to_file': {'backupCount': 1,
                                    'class': 'logging.handlers.RotatingFileHandler',
                                    'encoding': 'utf-8',
                                    'filename': 'prom.log',
                                    'formatter': 'formatter_1',
                                    'level': 'INFO',
                                    'maxBytes': 16384},
                        'to_mail': {'class': 'logging.handlers.SMTPHandler',
                                    'mailhost': SMTP_CONFIG.host.split(':'),
                                    'fromaddr': f'Prom data update <{SMTP_CONFIG.from_addr}>',
                                    'toaddrs': SMTP_CONFIG.to_addr,
                                    'subject': SMTP_CONFIG.subject,
                                    'credentials': SMTP_CONFIG.user_password,
                                    'formatter': 'formatter_1',
                                    'level': 'WARNING'},
                        },
           'root': {'handlers': ['to_console', 'to_file', 'to_mail'],
                    'level': 'INFO'}
           }

if __name__ == '__main__':
    print(f'HOST: {HOST}')
    print(f'PATH_PROM: {PATH_PROM}')
    print(f'SKIP_REAL: {SKIP_REAL}')
    print(f'DEBUG_MODE: {DEBUG_MODE}')
    print(f'AUTH_TOKEN_PRODUCTS: {AUTH_TOKEN_PRODUCTS}')
    print(f'PATH_BASE: {PATH_BASE}')
    print(f'LAST_PRODUCT_ID: {LAST_PRODUCT_ID}')
    print(f'SMTP_CONFIG: {SMTP_CONFIG}')
