# Коза :)
# https://github.com/evo-company/company-api-example/blob/master/python/api_python3-5_example.py
# Доступные методы API:
# https://prom.ua/cloud-cgi/static/uaprom-static/docs/swagger/index.html
# https://public-api.docs.prom.ua/#/

import http.client
import json
from typing import Union


class HTTPError(Exception):
    pass


class REQUESTError(Exception):
    pass


class PromClient:

    def __init__(self, host: str, token: str):
        self.host = host
        self.token = token
        self.connection = None

    def set_connection(self):
        self.connection = http.client.HTTPSConnection(self.host)

    def close_connection(self):
        if self.connection:
            self.connection.close()

    def make_request_with_conn(self, *args, **kwargs) -> dict:
        """
        The host (prom.ua) set a limit. It allows only five connections in a row.
        """
        try:
            self.set_connection()
            return self.make_request(*args, **kwargs)
        finally:
            self.close_connection()

    def make_request(self, method: str, url: str, body: Union[list, dict] = None) -> dict:
        """
        Needs wrapping, look: make_request_with_conn()
        """
        headers = {'Authorization': 'Bearer {}'.format(self.token),
                   'Content-type': 'application/json'}
        if body:
            body = json.dumps(body)

        self.connection.request(method, url, body=body, headers=headers)
        response = self.connection.getresponse()
        if response.status != 200:
            raise HTTPError('{}: {}'.format(response.status, response.reason))
        response_data = response.read()

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
        return self.make_request_with_conn(method, url)

    def get_product_id(self, _id: int) -> dict:
        url = f'/api/v1/products/{_id}'
        method = 'GET'
        return self.make_request_with_conn(method, url)

    def get_product_external_id(self, external_id: str) -> dict:
        url = f'/api/v1/products/by_external_id/{external_id}'
        method = 'GET'
        return self.make_request_with_conn(method, url)

    def set_products_list_id(self, products: list) -> dict:
        url = f'/api/v1/products/edit'
        method = 'POST'
        body = products
        return self.make_request_with_conn(method, url, body)

    def set_products_list_external_id(self, products_external_id: list) -> dict:
        """
        "id": "string",  <--- product_external_id
        """
        url = f'/api/v1/products/edit_by_external_id'
        method = 'POST'
        body = products_external_id
        return self.make_request_with_conn(method, url, body)


if __name__ == '__main__':
    pass
