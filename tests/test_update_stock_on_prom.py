from unittest import TestCase, skipIf

from prom_package.config import SKIP_REAL
from prom_package.update_stock_on_prom import write_products_prom


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
