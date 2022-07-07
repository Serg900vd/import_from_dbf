from pathlib import Path
from unittest import TestCase, skipIf

import yaml

from prom_package.config import SKIP_REAL, PATH_PROM, PATH_BASE
from prom_package.update_stock_on_prom import write_products_prom, read_products_prom, get_prom_chang_list
from uninet.get_data_uninet import BasePassDBF, CODEPAGE

PATH_TESTS = PATH_PROM.parent / 'tests'


@skipIf(SKIP_REAL, 'Skipping tests that hit the real API server.')
class TestWriteProductsProm(TestCase):
    def test_write_products_prom(self):
        products_changed_list = [{'external_id': 'test_HB770',
                                  'id': 1616486427,
                                  'presence': 'not_available',
                                  'price': 8.5,
                                  'prices': [{'minimum_order_quantity': 5.0, 'price': 8.0}],
                                  'status': 'not_on_display'},
                                 {'external_id': 'OL6',
                                  'id': 628473798,
                                  'presence': 'not_available',
                                  'price': 16.73,
                                  'prices': [{'minimum_order_quantity': 2.0, 'price': 15.06}],
                                  'status': 'on_display'},
                                 ]
        self.assertTrue(write_products_prom(products_changed_list))

    def test_write_products_prom_empty(self):
        self.assertFalse(write_products_prom([]))

    def test_write_products_prom_err(self):
        err_products_changed_list = [{'external_id': 'test_HB770',
                                      'id': 1616486427,
                                      'presence': 'ERRRORnot_available',
                                      'price': 8.5,
                                      'prices': [{'minimum_order_quantity': 5.0, 'price': 8.0}],
                                      'status': 'not_on_display'},
                                     {'external_id': 'OL6',
                                      'id': 628473798,
                                      'presence': 'not_available',
                                      'price': 16.73,
                                      'prices': [{'minimum_order_quantity': 2.0, 'price': 15.06}],
                                      'status': 'on_display'},
                                     ]
        self.assertRaises(ValueError, write_products_prom, err_products_changed_list)


@skipIf(SKIP_REAL, 'Skipping tests that hit the real API server.')
class TestReadProductsProm(TestCase):
    def test_read_products_prom(self):
        last_id = 637872504  # Gets a list with 21 items only
        products_prom = read_products_prom(last_id)
        path_data = PATH_TESTS / 'prom_test_data/read_products_prom_test.yaml'
        with open(Path(path_data)) as f:
            # yaml.dump(products_prom, f, default_flow_style=False)
            products_prom_test = yaml.safe_load(f)

        self.assertListEqual(products_prom_test, products_prom)


class TestGetPromChangedList(TestCase):
    def test_get_prom_changed_list(self):
        path_data = PATH_TESTS / 'prom_test_data/products_prom_test.yaml'
        with open(Path(path_data)) as f:
            products_prom_test = yaml.safe_load(f)

        path_data = PATH_TESTS / 'prom_test_data/products_changed_list_test.yaml'
        with open(Path(path_data)) as f:
            products_changed_list_test = yaml.safe_load(f)

        path_data = PATH_TESTS / 'prom_test_data/bd_test.yaml'
        with open(Path(path_data)) as f:
            bd_test = yaml.safe_load(f)

        bd = BasePassDBF(PATH_BASE, CODEPAGE, key_field_warehous='KOL_SKL', key_field_goods='SHOW_SITE')
        bd.goods = bd_test['goods']
        bd.warehous = bd_test['warehous']

        products_changed_list = get_prom_chang_list(bd, products_prom_test)
        self.assertListEqual(products_changed_list, products_changed_list_test)
