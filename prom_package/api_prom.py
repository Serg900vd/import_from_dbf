# Коза :)
# https://github.com/evo-company/company-api-example/blob/master/python/api_python3-5_example.py
# Доступные методы API:
# https://prom.ua/cloud-cgi/static/uaprom-static/docs/swagger/index.html
# https://public-api.docs.prom.ua/#/

import http.client
import json
import pprint

from prom_package.config import AUTH_TOKEN_READ, AUTH_TOKEN_WRITE
from prom_package.constants import HOST


class HTTPError(Exception):
    pass


class REQUESTError(Exception):
    pass


class PromClient:

    def __init__(self, host, token):
        self.host = host
        self.token = token
        self.connection = None

    def make_request(self, method, url, body=None):

        headers = {'Authorization': 'Bearer {}'.format(self.token),
                   'Content-type': 'application/json'}
        if body:
            body = json.dumps(body)

        try:
            self.connection = http.client.HTTPSConnection(self.host)
            self.connection.request(method, url, body=body, headers=headers)
            response = self.connection.getresponse()
            if response.status != 200:
                raise HTTPError('{}: {}'.format(response.status, response.reason))
            response_data = response.read()
        except:
            raise
        finally:
            if self.connection:
                self.connection.close()

        return json.loads(response_data.decode())

    def get_products_list(self, limit: int = None, last_id: int = None, group_id: int = None) -> dict:
        """
        Получить список товаров
        ! Больше 100 шт не выдает
        :param limit: int Ограничение количества товаров в ответе.
        :param last_id: int Ограничить выборку товаров с идентификаторами не выше указанного. Возвращает по 20шт
        :param group_id: int Идентификатор группы. По-умолчанию - идентификатор корневой группы компании.
        :return: dict
        """
        url = '/api/v1/products/list'
        method = 'GET'
        if limit or last_id or group_id:
            url = f'{url}?' + \
                  f'limit={limit}&' * bool(limit) + \
                  f'last_id={last_id}&' * bool(last_id) + \
                  f'group_id={group_id}' * bool(group_id)
        return self.make_request(method, url)

    def get_product_id(self, id: int):
        url = f'/api/v1/products/{id}'
        method = 'GET'
        return self.make_request(method, url)

    def get_product_external_id(self, external_id: str):
        url = f'/api/v1/products/by_external_id/{external_id}'
        method = 'GET'
        return self.make_request(method, url)

    def set_products_list_id(self, products: list):
        url = f'/api/v1/products/edit'
        method = 'POST'
        body = products
        return self.make_request(method, url, body)

    def set_products_list_external_id(self, products_external_id: list):
        """
        "id": "string",  <--- product_external_id
        """
        url = f'/api/v1/products/edit_by_external_id'
        method = 'POST'
        body = products_external_id
        return self.make_request(method, url, body)


def main_read():
    # Initialize Client
    if not AUTH_TOKEN_READ:
        raise Exception('Sorry, there\'s no any AUTH_TOKEN_READ!')
    api_prom = PromClient(HOST, AUTH_TOKEN_READ)

    # product_list = api_prom.get_products_list(2, group_id=81223949)
    # if not product_list['products']:
    #     raise Exception('Sorry, there\'s no any product!')
    # pprint.pprint(product_list)

    # test external_id 'test_HB770'
    product_item = api_prom.get_product_external_id('test_HB770')
    pprint.pprint(product_item)

    # test product id 1616486427
    # product_item = api_prom.get_product_id(1616486427)
    # pprint.pprint(product_item)

    # # Order example data. Requred to be setup to get example uninet
    # order_id = order_list['orders'][0]['id']
    # order_ids = [order_id]
    # status = 'received'
    #
    # # Setting order status
    # pprint.pprint(api_prom.set_order_status(status=status, ids=order_ids))
    #
    # # # Getting order by id
    # pprint.pprint(api_prom.get_order(order_id))


def main_write():
    # Initialize Client
    if not AUTH_TOKEN_WRITE:
        raise Exception('Sorry, there\'s no any AUTH_TOKEN_WRITE!')
    api_prom = PromClient(HOST, AUTH_TOKEN_WRITE)

    # test product id 1616486427
    # 'external_id' 'test_HB770' -- READ ONLY
    products_list = [{'id': 1616486427,
                      'external_id': 'test_HB770',
                      'presence': 'available',
                      'price': 8.5,
                      'prices': [{'minimum_order_quantity': 5.0, 'price': 7.0}],
                      'sku': 'test_HB770',
                      'status': 'on_display',
                      }]
    response = api_prom.set_products_list_id(products_list)
    pprint.pprint(response)


if __name__ == '__main__':
    # main_write()

    main_read()
