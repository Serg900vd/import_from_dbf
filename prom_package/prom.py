# The module updates the product data on the prom.ua website according to the local dbf database.
# The following parameters are updated: visibility status, availability status, prices.
#
# You need to create a settings file "config_prom.txt" in the following format:
# {
#  "HOST": "my.prom.ua",
#  "AUTH_TOKEN_PRODUCTS": "my_token",
#  "PATH_BASE": "path_to_base",
#  "LAST_PRODUCT_ID": int_last_product_id_on_prom_catalog
# }
import logging
import logging.config
from dataclasses import dataclass, field, asdict
from time import time
from typing import List, Literal

from prom_package.api_prom import PromClient
from prom_package.config import PATH_BASE, AUTH_TOKEN_PRODUCTS, LAST_PRODUCT_ID, HOST, DEBUG_MODE, LOGGING
from prom_package.smtp import send_email
from uninet.get_data_uninet import BasePassDBF, CODEPAGE

# Status constants
Status = Literal[
    'on_display', 'draft', 'deleted', 'not_on_display', 'editing_required', 'approval_pending', 'deleted_by_moderator']
STATUS_ON_DISPLAY: Status = 'on_display'
NOT_ON_DISPLAY: Status = 'not_on_display'

# Presence constants
Presence = Literal['available', 'not_available', 'order', 'service', 'waiting']
PRESENCE_AVAILABLE: Presence = 'available'
PRESENCE_NOT_AVAILABLE: Presence = 'not_available'


@dataclass
class Product:
    id: int = 0
    external_id: str = ''
    presence: Presence = PRESENCE_NOT_AVAILABLE
    price: float = 0.0
    prices: List[dict] = field(default_factory=list)
    status: Status = NOT_ON_DISPLAY

    def __post_init__(self, ):
        if not self.prices:
            self.prices.append({'minimum_order_quantity': 0.0, 'price': 0.0})

    def set_price_min_order(self, quantity):
        self.prices[0]['minimum_order_quantity'] = quantity

    def set_price_d(self, price_d):
        self.prices[0]['price'] = price_d

    def get_price_d(self):
        return self.prices[0]['price']


def read_products_prom(last_id: int) -> List[dict]:
    """
    Download the current list of products from the site.
    Iterations in 20 pcs. starting from the last (last_id) in reverse order.
    :param last_id:
    :return:
    """
    # A query without parameters returns a list with only 100 products.
    # There is no way to get the whole list.
    api_prom = PromClient(HOST, AUTH_TOKEN_PRODUCTS)
    product_lust_id = api_prom.get_product_id(last_id)  # last =1616486427  first = 628464896
    products_prom = [product_lust_id['product']]

    logging.info('Start read_products_prom:')
    while True:
        products_20 = api_prom.get_products_list(last_id=last_id)
        products_20 = products_20['products']
        if not products_20:
            break
        products_prom += products_20
        last_id = products_prom[-1]['id']

        logging.debug('Prom read products: %s', len(products_prom))
    logging.info('Finish read_products_prom:')
    return products_prom


def load_bd() -> BasePassDBF:
    """
    Load the tables warehous.dbf, invoice.DBF, goods.dbf, firm.dbf from the dbf database.
    :return:
    """
    bd = BasePassDBF(PATH_BASE, CODEPAGE, key_field_warehous='KOL_SKL', key_field_goods='SHOW_SITE')
    bd.load_tables_dbf()
    return bd


def get_prom_chang_list(bd: BasePassDBF, products_prom: list) -> list:
    """
    Go through the list of goods, find products with changes.
    :param bd:
    :param products_prom:
    :return:
    """
    products_chang_list = []
    for p in products_prom:
        product_prom = Product(p['id'], p['external_id'], p['presence'], p['price'], p['prices'], p['status'])

        group_cod = p['external_id']
        presence = PRESENCE_AVAILABLE if bd.is_product_on_stock(group_cod) else PRESENCE_NOT_AVAILABLE
        product_bd = Product(p['id'], group_cod, presence)
        try:
            if bd.goods[group_cod]['show_site']:
                product_bd.status = STATUS_ON_DISPLAY
            else:
                product_bd.status = NOT_ON_DISPLAY
            product_bd.price = bd.goods[group_cod]['price_sale']
            price_d = bd.goods[group_cod]['price_d']
        except KeyError:
            product_bd.status = NOT_ON_DISPLAY
            product_bd.price = p['price']
            price_d = p['prices'][0]['price']

        product_bd.set_price_min_order(p['prices'][0]['minimum_order_quantity'])
        product_bd.set_price_d(price_d)

        if product_prom != product_bd:
            products_chang_list.append(asdict(product_bd))

    logging.info('%s products with changes', len(products_chang_list))
    # logging.debug('products_changed_list = %s', products_chang_list)
    return products_chang_list


def write_products_prom(products_changed_list: list) -> bool:
    """
    Record products with changes on Prom
    :param products_changed_list:
    :return:
    """
    if products_changed_list:
        api_prom = PromClient(HOST, AUTH_TOKEN_PRODUCTS)
        response = api_prom.set_products_list_id(products_changed_list)
        logging.info('processed_ids: %s', response['processed_ids'])
        if response['errors']:
            logging.warning('ERRORS: %s', response['errors'])
            raise ValueError(f'errors: {response["errors"]}')
        return True
    else:
        logging.info('products_changed_list is empty %s', products_changed_list)
        return False


def _logging_config():
    logging.config.dictConfig(LOGGING)
    if DEBUG_MODE:
        logging.root.setLevel('DEBUG')
        for handler in logging.root.handlers:
            if handler.name == 'to_console':
                handler.setLevel('DEBUG')


def main():
    _logging_config()
    time_start = time()
    logging.info('----START----')

    try:
        # Get an up-to-date list of goods from the site prom.ua
        last_id = LAST_PRODUCT_ID
        # last_id = 637872504  # Gets a list with 21 items only
        products_prom = read_products_prom(last_id)

        # Load the tables warehous.dbf, invoice.DBF, goods.dbf, firm.dbf from the dbf database
        bd = load_bd()

        # Find products with changes
        products_changed_list = get_prom_chang_list(bd, products_prom)

        # Record products with changes on Prom
        write_products_prom(products_changed_list)
    except Exception as exc:
        # import traceback
        # send_email(traceback.format_exc())

        logging.warning(f'Houston we have a problem >> {exc}', exc_info=True, stack_info=True)


    time_run = time() - time_start
    logging.info('----FINISH----\n----RUN TIME: %s s.', time_run)
    # if DEBUG_MODE:
    #     pause = input('OK?')


if __name__ == '__main__':
    # To compile .exe file:
    # !!! For Windows 7 64x Python 3.8 + Pyinstaller-5.0.1 only !!!
    #  config.py set: PATH_PROM = Path.cwd()
    #  Command:
    #   pyinstaller prom.py --onefile

    main()
