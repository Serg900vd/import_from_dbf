import json

from pathlib import Path

# Read the start path
PATH_PROM = Path(__file__).parent

# To compile .exe file
# PATH_PROM = Path.cwd()

# Test base setting
PATH_BASE_TEST = Path("../tests/dbf/")

# For skipping tests that hit the real API server.
SKIP_REAL = False

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
    print(f'AUTH_TOKEN_PRODUCTS: {AUTH_TOKEN_PRODUCTS}')
    print(f'PATH_BASE: {PATH_BASE}')
    print(f'LAST_PRODUCT_ID: {LAST_PRODUCT_ID}')

    pass
