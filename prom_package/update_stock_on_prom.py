#
import pprint
from dataclasses import dataclass, field, asdict
from typing import List

from prom_package.api_prom import PromClient
from prom_package.config import PATH_BASE, AUTH_TOKEN_PRODUCTS, LAST_PRODUCT_ID, HOST
from uninet.get_data_uninet import BasePassDBF, CODEPAGE

# Status constants
STATUS_ON_DISPLAY = 'on_display'
NOT_ON_DISPLAY = 'not_on_display'

# Presence constants
PRESENCE_AVAILABLE = 'available'
PRESENCE_NOT_AVAILABLE = 'not_available'


# @dataclass
# class Product:
#     id: int
#     external_id: str
#     presence: Presence = Presence.NOT_AVAILABLE
#     price: float = 0.0
#     prices: List[dict] = field(default_factory=list)
#     status: Status = Status.DRAFT
#
#     def _init__(self):
#         self.prices = [{'minimum_order_quantity': 0.0, 'price': 0.0}]
#
#     def price_d(self, price_d):
#         self.prices[0]['price'] = price_d

def read_products_prom() -> List[dict]:
    """
    Загружаем актуальный список товаров с сайта.
    По 20шт. начиная с последнего (last_id)
    """
    api_prom = PromClient(HOST, AUTH_TOKEN_PRODUCTS)
    product_lust_id = api_prom.get_product_id(last_id)  # last =1616486427  first = 628464896
    products_prom = [product_lust_id['product']]

    print(f'Prom read products:')
    while True:
        products_20 = api_prom.get_products_list(last_id=last_id)
        products_20 = products_20['products']
        if not products_20:
            break
        products_prom += products_20
        last_id = products_prom[-1]['id']

        print(len(products_prom), end=', ')
    print(' ')
    return products_prom


def load_bd() -> BasePassDBF:
    """
    Загружаем из базы dbf таблицы warehous.dbf, invoice.DBF, goods.dbf, firm.dbf
    :return:
    """
    bd = BasePassDBF(PATH_BASE, CODEPAGE, key_field_warehous='KOL_SKL', key_field_goods='SHOW_SITE')
    bd.load_tables_dbf()
    return bd


def get_prom_chang_list(bd: BasePassDBF, products_prom: list) -> list:
    """
    Проходим по списку товаров, находим с изменениями.
    :param bd:
    :param products_prom:
    :return:
    """
    products_chang_list = []
    for p in products_prom:
        product_prom = {'id': p['id'], 'external_id': p['external_id'], 'presence': p['presence'], 'price': p['price'],
                        'prices': p['prices'], 'status': p['status']}
        id = p['id']
        group_cod = p['external_id']
        presence = PRESENCE_AVAILABLE if bd.is_product_on_stock(group_cod) else PRESENCE_NOT_AVAILABLE
        try:
            if bd.goods[group_cod]['show_site']:
                status = STATUS_ON_DISPLAY
            else:
                status = NOT_ON_DISPLAY
            price = bd.goods[group_cod]['price_sale']
            price_d = bd.goods[group_cod]['price_d']
        except KeyError:
            status = NOT_ON_DISPLAY
            price = p['price']
            price_d = p['prices'][0]['price']

        prices = [{'minimum_order_quantity': p['prices'][0]['minimum_order_quantity'], 'price': price_d}]
        product_bd = {'id': id, 'external_id': group_cod, 'presence': presence, 'price': price, 'prices': prices,
                      'status': status}
        if product_prom != product_bd:
            products_chang_list.append(product_bd)

    print(f'{len(products_chang_list)} products with changes')

    return products_chang_list


def write_products_prom(products_changed_list: list) -> bool:
    """
    Записываем продукты с изменениями на Prom
    """
    if products_changed_list:
        api_prom = PromClient(HOST, AUTH_TOKEN_PRODUCTS)
        response = api_prom.set_products_list_id(products_changed_list)
        print(response)
        if response['errors']:
            raise ValueError(f'errors: {response["errors"]}')
        return True
    else:
        print(f'products_changed_list is empty {products_changed_list}')
        return False


def main():
    # Получаем актуальный список товаров с сайта prom.ua
    last_id = LAST_PRODUCT_ID
    # last_id = 637872504  # Gets a list with 21 items only
    products_prom = read_products_prom(last_id)

    # Загружаем из базы dbf таблицы warehous.dbf, invoice.DBF, goods.dbf, firm.dbf
    bd = load_bd()

    # Находим продукты с изменениями
    products_changed_list = get_prom_chang_list(bd, products_prom)
    pprint.pprint(f'products_changed_list = {products_changed_list}')

    # Записываем продукты с изменениями на Prom
    write_products_prom(products_changed_list)


if __name__ == '__main__':
    #  prom_package
    #  pyinstaller update_stock_on_prom.py --onefile

    main()
    pause = input('OK?')
