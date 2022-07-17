import json
import logging.config

from pathlib import Path

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

# Logging configuration by dictConfig
_format = '%(asctime)s [%(name)s] %(module)s.%(levelname)s: %(message)s'
LOGGING = {'version': 1,
           'formatters': {'formatter_0': {'datefmt': '%d/%m/%Y %H:%M:%S',
                                          'format': _format
                                          }
                          },
           'handlers': {'to_console': {'class': 'logging.StreamHandler',
                                       'formatter': 'formatter_0',
                                       'level': 'WARNING'},
                        'to_file': {'backupCount': 1,
                                    'class': 'logging.handlers.RotatingFileHandler',
                                    'encoding': 'utf-8',
                                    'filename': 'update_stock_on_prom.log',
                                    'formatter': 'formatter_0',
                                    'level': 'INFO',
                                    'maxBytes': 8192}},
           'loggers': {'prom': {'handlers': ['to_console', 'to_file'],
                                'level': 'WARNING'}}
           }

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('prom')
if DEBUG_MODE:
    logger.setLevel('DEBUG')
    for handler in logger.handlers:
        if handler.name == 'to_console':
            handler.setLevel(level='DEBUG')

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

if __name__ == '__main__':
    print(f'HOST: {HOST}')
    print(f'PATH_PROM: {PATH_PROM}')
    print(f'SKIP_REAL: {SKIP_REAL}')
    print(f'DEBUG_MODE: {DEBUG_MODE}')
    print(f'AUTH_TOKEN_PRODUCTS: {AUTH_TOKEN_PRODUCTS}')
    print(f'PATH_BASE: {PATH_BASE}')
    print(f'LAST_PRODUCT_ID: {LAST_PRODUCT_ID}')

    pass
