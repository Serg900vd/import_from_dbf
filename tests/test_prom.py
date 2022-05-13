import copy
from unittest import TestCase
from unittest import skipIf

from prom_package.config import AUTH_TOKEN_WRITE
from prom_package.constants import SKIP_REAL
from prom_package.prom import PromClient, REQUESTError

# Product id 1616486427 for tests...
PRODUCT_ID_1616486427 = {'id': 1616486427,
                         'external_id': 'test_HB770',  # -- READ ONLY
                         'presence': 'available',
                         'price': 8.5,
                         'prices': [{'minimum_order_quantity': 5.0, 'price': 8.0}],
                         'sku': 'test_HB770',  # -- READ ONLY
                         'status': 'on_display',
                         }
RESET_PRODUCT_ID_1616486427 = {'id': 1616486427,
                               'external_id': 'test_HB770',  # -- READ ONLY
                               'presence': 'not_available',
                               'price': 0.5,
                               'prices': [{'minimum_order_quantity': 2.0, 'price': 0.1}],
                               'sku': 'test_HB770',  # -- READ ONLY
                               'status': 'draft',
                               }
PRODUCT_KEYS = {'keywords', 'status', 'is_variation', 'sku', 'variation_base_id', 'presence', 'external_id',
                'selling_type', 'prices', 'price', 'group', 'currency', 'minimum_order_quantity', 'measure_unit',
                'images', 'date_modified', 'variation_group_id', 'description', 'main_image', 'discount',
                'quantity_in_stock', 'regions', 'category', 'name', 'id', 'name_multilang'}


# Run tests for integration contract on the real API server
@skipIf(SKIP_REAL, 'Skipping tests that hit the real API server.')
class TestIntegrationContractPromProduct(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Initialize Client
        cls.api_prom = PromClient(AUTH_TOKEN_WRITE)

    def test_1_product_keys(self):
        product_received = self.api_prom.get_product_id(1616486427)['product']
        keys_received_set = set(product_received.keys())
        keys_test = set(PRODUCT_KEYS).issubset(keys_received_set)
        self.assert_(keys_test, f'Missing these product keys {PRODUCT_KEYS - keys_received_set}')

    def test_2_reset_product_id_1616486427(self):
        product_set = RESET_PRODUCT_ID_1616486427
        response = self.api_prom.set_products_list_id([product_set])
        if response['errors'] != {}:
            raise REQUESTError(response)
        product_received = self.api_prom.get_product_id(1616486427)['product']
        # Value test
        for key, value in product_set.items():
            self.assertEquals(value, product_received[key], f'Parameter {key} : {value} is not set')

    def test_3_set_product_id_1616486427(self):
        product_set = PRODUCT_ID_1616486427
        response = self.api_prom.set_products_list_id([product_set])
        if response['errors'] != {}:
            raise REQUESTError(response)
        product_received = self.api_prom.get_product_id(1616486427)['product']
        # Value test
        for key, value in product_set.items():
            self.assertEqual(value, product_received[key], f'Parameter {key} : {value} is not set')

    def test_4_is_not_set_parametr_sku(self):
        product_set = copy.copy(PRODUCT_ID_1616486427)
        product_set['sku'] = 'RESET'  # parameter 'sku' is read only
        response = self.api_prom.set_products_list_id([product_set])
        if response['errors'] != {}:
            raise REQUESTError(response)
        product_received = self.api_prom.get_product_id(1616486427)['product']
        self.assertNotEqual(product_received['sku'], 'RESET')
