import json
from typing import List

from prom_package.api_prom import PromClient
from prom_package.config import AUTH_TOKEN_PRODUCTS, LAST_PRODUCT_ID, HOST


def temp_():
    # Загружаем актуальный список товаров с сайта
    last_id = LAST_PRODUCT_ID
    api_prom = PromClient(HOST, AUTH_TOKEN_PRODUCTS)
    product_lust_id = api_prom.get_product_id(last_id)  # last =1616486427  first = 628464896
    products_prom = [product_lust_id['product']]

    # last_id = 628472731 # Ограничить список
    while True:
        products_20 = api_prom.get_products_list(last_id=last_id)
        products_20 = products_20['products']
        if not products_20:
            break
        products_prom += products_20
        last_id = products_prom[-1]['id']

        print(f'Prom read {len(products_prom)} products')

    products_prom = products_prom[:25]
    products_prom.sort(key=lambda x: x['id'])
    with open('prom_recurse\\prom_products.json', 'w') as f:
        # for line in products_prom:
        # f.write(f"{line['id']}\n")
        products_prom_json = json.dumps(products_prom)
        f.write(products_prom_json)

    with open('prom_recurse\\prom_products.json') as f:
        products_prom_json_r = f.read()
        products_prom_r = json.loads(products_prom_json_r)

    if products_prom_r == products_prom:
        print('Ok')
    pass
    d = 4 * 5


def read_products_prom() -> List[dict]:
    """
    Загружаем актуальный список товаров с сайта
    """
    last_id = LAST_PRODUCT_ID
    api_prom = PromClient(HOST, AUTH_TOKEN_PRODUCTS)
    product_lust_id = api_prom.get_product_id(last_id)  # last =1616486427  first = 628464896
    products_prom = [product_lust_id['product']]

    last_id = 637872504  # Ограничить список
    print('last_id = 637872504 # Ограничить список')
    while True:
        products_20 = api_prom.get_products_list(last_id=last_id)
        products_20 = products_20['products']
        if not products_20:
            break
        products_prom += products_20
        last_id = products_prom[-1]['id']

        print(f'Prom read {len(products_prom)} products')
    return products_prom


if __name__ == '__main__':
    read_products_prom()
