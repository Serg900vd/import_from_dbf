import copy
from unittest import TestCase
from unittest import skipIf

from prom_package.config import AUTH_TOKEN_WRITE
from prom_package.constants import SKIP_REAL
from prom_package.prom import PromClient, REQUESTError

# Product id 1616486427 for tests...
ID_1616486427 = {'id': 1616486427,
                 'external_id': 'test_HB770',  # -- READ ONLY
                 'presence': 'available',
                 'price': 8.5,
                 'prices': [{'minimum_order_quantity': 5.0, 'price': 8.0}],
                 'sku': 'test_HB770',  # -- READ ONLY
                 'status': 'on_display',
                 }
RESET_ID_1616486427 = {'id': 1616486427,
                       'external_id': 'test_HB770',  # -- READ ONLY
                       'presence': 'not_available',
                       'price': 0.5,
                       'prices': [{'minimum_order_quantity': 2.0, 'price': 0.1}],
                       'sku': 'test_HB770',  # -- READ ONLY
                       'status': 'draft',
                       }


@skipIf(SKIP_REAL, 'Skipping tests that hit the real API server.')
# Run tests for integration contract on the real API server
class TestIntegrationContract(TestCase):
    def test_1_product_keys(self):
        # TODO Keys test
        # keys_test = set(product_sent.keys()).issubset(set(product_received.keys()))
        # self.assert_(keys_test,'')
        pass

    def test_2_reset_product_id_1616486427(self):
        api_prom = PromClient(AUTH_TOKEN_WRITE)
        product_sent = RESET_ID_1616486427
        response = api_prom.set_products_list_id([product_sent])
        if response['errors'] != {}:
            raise REQUESTError(response)
        product_received = api_prom.get_product_id(1616486427)['product']
        # Value test
        for key, value in product_sent.items():
            self.assertEquals(value, product_received[key], f'Parameter {key} : {value} is not set')

    def test_3_set_product_id_1616486427(self):
        api_prom = PromClient(AUTH_TOKEN_WRITE)
        product_sent = ID_1616486427
        response = api_prom.set_products_list_id([product_sent])
        if response['errors'] != {}:
            raise REQUESTError(response)
        product_received = api_prom.get_product_id(1616486427)['product']
        # Value test
        for key, value in product_sent.items():
            self.assertEqual(value, product_received[key], f'Parameter {key} : {value} is not set')

    def test_4_is_not_set_parametr_sku(self):
        api_prom = PromClient(AUTH_TOKEN_WRITE)
        product_sent = copy.copy(ID_1616486427)
        product_sent['sku'] = 'RESET'  # parameter 'sku' is read only
        response = api_prom.set_products_list_id([product_sent])
        if response['errors'] != {}:
            raise REQUESTError(response)
        product_received = api_prom.get_product_id(1616486427)['product']

        self.assertNotEqual(product_received['sku'], 'RESET')
