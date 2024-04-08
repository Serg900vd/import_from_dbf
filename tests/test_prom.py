import logging
from pathlib import Path
from typing import Union
from unittest import TestCase, skipIf
from unittest.mock import patch, Mock

import yaml

from prom_package.config import SKIP_REAL, PATH_PROM, DEBUG_MODE
from prom_package.prom import PromClient, write_products_prom, read_products_prom, get_prom_chang_list
from uninet.get_data_uninet import BasePassDBF

if DEBUG_MODE:
    logging.root.setLevel('DEBUG')
PATH_TESTS = PATH_PROM.parent / 'tests'
PATH_TESTS_DATA = PATH_TESTS / 'prom_test_data'


def read_yaml(file: str) -> Union[list, dict]:
    path_data = PATH_TESTS_DATA / file
    with open(path_data) as f:
        return yaml.safe_load(f)


@skipIf(SKIP_REAL, 'Skipping tests that hit the real API server.')
class TestWriteProductsPromOnRealAPI(TestCase):
    def test_write_products_prom(self):
        products_changed_list = read_yaml('test_write_products_prom.yaml')
        self.assertTrue(write_products_prom(products_changed_list))

    def test_write_products_prom_err(self):
        err_products_changed_list = read_yaml('test_write_products_prom_err.yaml')
        self.assertRaises(ValueError, write_products_prom, err_products_changed_list)


class TestWriteProductsProm(TestCase):
    @patch.object(PromClient, 'set_products_list_id')
    def test_write_products_prom(self, get_mock: Mock):
        get_mock.return_value = read_yaml('mock_set_products_list_id.yaml')
        products_changed_list = read_yaml('test_write_products_prom.yaml')
        self.assertTrue(write_products_prom(products_changed_list))
        get_mock.assert_called_with(products_changed_list)

    @patch.object(PromClient, 'set_products_list_id')
    def test_write_products_prom_err(self, get_mock):
        get_mock.return_value = read_yaml('mock_set_products_list_id_err.yaml')
        err_products_changed_list = read_yaml('test_write_products_prom_err.yaml')
        self.assertRaises(ValueError, write_products_prom, err_products_changed_list)
        get_mock.assert_called_with(err_products_changed_list)

    def test_write_products_prom_empty(self):
        self.assertFalse(write_products_prom([]))

# @skipIf(SKIP_REAL, 'Skipping tests that hit the real API server.')
# class TestReadProductsPromOnRealAPI(TestCase):
#     def test_onreal_read_products_prom(self):
#         last_id = 637872504  # Gets a list with 21 items only
#         products_prom = read_products_prom(last_id)
#         products_prom_test = read_yaml('test_onreal_read_products_prom_637872504.yaml')
#
#         # self.assertListEqual(products_prom_test, products_prom)
#         self.assertEqual(21, len(products_prom))


def mock_get_product_id():
    def _get_product_id(self, last_id):
        return read_yaml('637949599_get_product_id.yaml') if last_id == 637949599 else None

    return _get_product_id


def mock_get_products_list():
    def _get_products_list(self, last_id):
        id_list = [628464896, 636197521, 637874961, 637949599]
        if last_id not in id_list:
            return None
        return read_yaml(f'{last_id}_get_products_list.yaml')

    return _get_products_list


class TestReadProductsProm(TestCase):
    @patch('prom_package.api_prom.PromClient.get_products_list', new_callable=mock_get_products_list)
    @patch('prom_package.api_prom.PromClient.get_product_id', new_callable=mock_get_product_id)
    def test_read_products_prom(self, get_mock_id, get_mock_list):
        last_id = 637949599
        products_prom_test = read_yaml('test_read_products_prom_637949599.yaml')
        products_prom = read_products_prom(last_id)
        # with open(PATH_TESTS_DATA / 'test_read_products_prom_637949599.yaml', 'w') as f:
        #     yaml.dump(products_prom, f, default_flow_style=False)

        self.assertListEqual(products_prom_test, products_prom)


# class TestGetPromChangedList(TestCase):
#     def test_get_prom_changed_list(self):
#         products_prom_test = read_yaml('products_prom_test.yaml')
#         products_changed_list_test = read_yaml('products_changed_list_test.yaml')
#         # Get an instance of the class, parameters do not matter.
#         bd = BasePassDBF(Path('PATH_BASE'), 'CODEPAGE')
#         bd_test = read_yaml('bd_test.yaml')
#         bd.goods = bd_test['goods']
#         bd.warehous = bd_test['warehous']
#
#         products_changed_list = get_prom_chang_list(bd, products_prom_test)
#         self.assertListEqual(products_changed_list, products_changed_list_test)


class TestLogging(TestCase):
    def test_logging(self):
        logging.debug('TestLogging')
