# https://github.com/evo-company/company-api-example/blob/master/python/api_python3-5_example.py
# Доступные методы API:
# https://prom.ua/cloud-cgi/static/uaprom-static/docs/swagger/index.html

import http.client
import json
import pprint

from config import AUTH_TOKEN
from config import HOST


class HTTPError(Exception):
    pass


class PromClient(object):

    def __init__(self, token):
        self.token = token

    def make_request(self, method, url, body=None):
        connection = http.client.HTTPSConnection(HOST)

        headers = {'Authorization': 'Bearer {}'.format(self.token),
                   'Content-type': 'application/json'}
        if body:
            body = json.dumps(body)

        connection.request(method, url, body=body, headers=headers)
        response = connection.getresponse()
        if response.status != 200:
            raise HTTPError('{}: {}'.format(response.status, response.reason))

        response_data = response.read()
        return json.loads(response_data.decode())

    def get_products_list(self, limit: int = None, last_id: int = None, group_id: int = None) -> dict:
        """
        Получить список товаров
        :param limit: int Ограничение количества товаров в ответе.
        :param last_id: int Ограничить выборку товаров с идентификаторами не выше указанного.
        :param group_id: int Идентификатор группы. По-умолчанию - идентификатор корневой группы компании.
        :return: dict
        """
        url = '/api/v1/products/list'
        method = 'GET'
        if limit or last_id or group_id:
            url = f'{url}?' + f'limit={limit}&' * bool(limit) + f'last_id={last_id}&' * bool(
                last_id) + f'group_id={group_id}' * bool(group_id)
        return self.make_request(method, url)


def main():
    # Initialize Client
    if not AUTH_TOKEN:
        raise Exception('Sorry, there\'s no any AUTH_TOKEN!')

    api_prom = PromClient(AUTH_TOKEN)

    product_list = api_prom.get_products_list(2, group_id=81223949)
    if not product_list['products']:
        raise Exception('Sorry, there\'s no any product!')

    pprint.pprint(product_list)

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


if __name__ == '__main__':
    main()
