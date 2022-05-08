# https://github.com/evo-company/company-api-example/blob/master/python/api_python3-5_example.py
# Доступные методы API:
# https://prom.ua/cloud-cgi/static/uaprom-static/docs/swagger/index.html

import json
import http.client
import pprint
from pickle import GET

from aenum import Enum

from config import HOST
from config import AUTH_TOKEN


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

    def get_products_list(self, limit=None):
        url = '/api/v1/products/list'
        method = 'GET'
        if limit:
            url = f'{url}?limit={limit}'
        return self.make_request(method, url)


def main():
    # Initialize Client
    if not AUTH_TOKEN:
        raise Exception('Sorry, there\'s no any AUTH_TOKEN!')

    api_prom = PromClient(AUTH_TOKEN)

    product_list = api_prom.get_products_list(5)
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
