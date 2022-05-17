import datetime
import os
from unittest import TestCase, main

from uninet import get_data_uninet
from uninet.get_data_uninet import BasePassDBF

if os.getcwd().split('\\')[-1] == 'tests':
    PATH_BASE_TEST = "dbf\\"
else:
    PATH_BASE_TEST = "tests\\dbf\\"

CODEPAGE = 'cp1251'
FILTR_FIRM_UNINET_HB = (150, 183)
FILTER_GROUP_KM_HB = ('KM', 'HB')


class TestBasePassDBF_a(TestCase):
    def setUp(self) -> None:
        # Initialize Base Data
        self.bd = BasePassDBF(PATH_BASE_TEST, CODEPAGE)

    def test_set_firm_uninet_hb(self):
        self.bd.set_firm((150, 183))
        self.assertEqual(self.bd.firm, {150: 'Uninet USA', 183: 'H&B'})
        self.assertNotEqual(self.bd.firm, {150: 'Uninet USA', 184: 'H&B'})

    def test_set_firm_katun(self):
        self.bd.set_firm((7,))
        self.assertEqual(self.bd.firm, {7: 'Katun'})


class TestBasePassDBF_b(TestCase):
    bd = None

    @classmethod
    def setUpClass(cls):
        # Initialize Base Data
        cls.bd = BasePassDBF(PATH_BASE_TEST, CODEPAGE, key_field_warehous='KOL_SKL')
        cls.bd.load_tables_dbf()

    def test_load_tables_dbf(self):
        self.assert_(self.bd.warehous)
        self.assert_(self.bd.invoice)
        self.assert_(self.bd.goods)
        self.assert_(self.bd.firm)

    def test_get_warehous_grcod_filter(self):
        _result = [
            {'inv': 'DBL8', 'group': 'KM', 'cod': 1129, 'kol': 2, 'price_usd': 1.0, 'price_inv': 0.0, 'kol_skl': 5,
             'kol_rezerv': 0, 'kol_sale': 0, 'kol_sf': 0, 'kol_otkaz': 0, 'code': 'KM1129DBL8', 'price_krb': 89.44,
             'tax_tam': None, 'tax_ack': None, 'size_inv': '', 'size_skl': '', 'old_sale': 0}]

        self.assertEqual(self.bd.get_warehous_grcod_filter('KM1129')[0], _result[0])

    def test_get_warehous_grcod_sum(self):
        _result = {'group_cod': 'KM1129', 'kol': 2, 'kol_otkaz': 0, 'kol_rezerv': 0, 'kol_sale': 0, 'kol_sf': 0,
                   'kol_skl': 5, 'old_sale': 0}
        aa = self.bd.get_warehous_grcod_sum('KM1129')
        self.assertEqual(self.bd.get_warehous_grcod_sum('KM1129'), _result)
        pass


class TestBasePassDBF_get_data_from_pass(TestCase):
    # The method get_data_from_pass() is @classmethod
    def test_warehous(self):
        _result = {'cod': 1196,
                   'code': 'KM1196DBL8',
                   'group': 'KM',
                   'inv': 'DBL8',
                   'kol': 3,
                   'kol_otkaz': 0,
                   'kol_rezerv': 0,
                   'kol_sale': 0,
                   'kol_sf': 0,
                   'kol_skl': 4,
                   'old_sale': 0,
                   'price_inv': 0.0,
                   'price_krb': 136.26,
                   'price_usd': 1.0,
                   'size_inv': '',
                   'size_skl': '',
                   'tax_ack': None,
                   'tax_tam': None}
        self.assertEqual(
            BasePassDBF.get_data_from_pass(PATH_BASE_TEST + 'warehous.dbf', CODEPAGE, key_field='KOL_SKL',
                                           filter_group=FILTER_GROUP_KM_HB)['KM1196DBL8'], _result)

    def test_goods(self):
        _result = {'cod': 1196,
                   'cond_id': 0,
                   'cond_str': '          ',
                   'curr': '   ',
                   'dsn_id': 0,
                   'firm': 150,
                   'group': 'KM',
                   'groupid': 786,
                   'kpr1': 0.0,
                   'kpr2': 0.0,
                   'kpr3': 0.0,
                   'kpr4': 0.0,
                   'kpr5': 0.0,
                   'label_txt': '                              ',
                   'mark': ' ',
                   'min_qty': 0,
                   'model': '21284               ',
                   'model_txt': 'Xerox Phaser 6510 WC 6515 Чорний Тонер 105g/5500стор Black '
                                'toner                                    ',
                   'price_a': 0.0,
                   'price_b': 9.5,
                   'price_bas': 0.0,
                   'price_c': 9.8,
                   'price_d': 10.0,
                   'price_dm': 0.0,
                   'price_opt': 0.0,
                   'price_sale': 11.0,
                   'prod_code': '3707909000  ',
                   'profit': 0,
                   'public_mod': 'Xerox Phaser 6510 WC 6515 Черный Тонер 105g/5500стр Black '
                                 'toner',
                   'public_txt': 'Произведен и расфасован в США.',
                   'show_prg': True,
                   'show_site': True,
                   'size': 0,
                   'tax_ack': 0,
                   'tax_tam': 0,
                   'testico': 1,
                   'url': '',
                   'warranty': 0}
        self.assertEqual(
            BasePassDBF.get_data_from_pass(PATH_BASE_TEST + 'goods.dbf', CODEPAGE,
                                           key_tabl=lambda row: row.GROUP + str(row.COD), key_field='SHOW_PRG',
                                           filter_group=FILTER_GROUP_KM_HB)['KM1196'], _result)

    def test_invoice(self):
        _result = {'app_num': 0,
                   'auto_id': 0,
                   'cond': 0,
                   'condition': '          ',
                   'contract': '                    ',
                   'curr': '001',
                   'cust': 1377,
                   'dm_usd': 1.0,
                   'inv': 'DBM1',
                   'inv_day': datetime.date(2022, 2, 10),
                   'inv_nkl': 486848,
                   'inv_reg': datetime.date(2022, 2, 10),
                   'inv_txt': 'лидер сч 54                                       ',
                   'krb_usd': 1.0,
                   'notes': '',
                   'peo': 0,
                   'sum_inv': 0.0,
                   'sum_krb': 11812.5,
                   'sum_usd': 502.65,
                   'taking_day': None,
                   'tax_nds': 1,
                   'tax_proc': 1.0,
                   'tax_tam': 0,
                   'user_id': 22}
        self.assertEqual(
            BasePassDBF.get_data_from_pass(PATH_BASE_TEST + 'invoice.DBF', CODEPAGE, lambda row: row.INV)[
                'DBM1'], _result)


class Test_Main_uninet(TestCase):
    def test_main_uninet(self):
        file_name = 'stock_uninet.csv'
        get_data_uninet.main_uninet(PATH_BASE_TEST, file_name)
        with open(PATH_BASE_TEST + file_name) as test, open(PATH_BASE_TEST + 'backup\\' + file_name) as pattern:
            file_test = test.read()
            file_pattern = pattern.read()

        self.assertEqual(file_test, file_pattern)


if __name__ == '__main__':
    main()
