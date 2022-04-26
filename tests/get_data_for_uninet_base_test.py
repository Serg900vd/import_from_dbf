from unittest import TestCase, main
import doctest, os
from work import get_data_for_uninet_base

if os.getcwd().split('\\')[-1] == 'tests':
    PATH_BASE_TEST = "dbf\\"
else:
    PATH_BASE_TEST = "tests\\dbf\\"

CODEPAGE = 'cp1251'
FILTR_FIRM_UNINET_HB = (150, 183)
FILTER_GROUP_KM_HB = ('KM', 'HB')


class Get_firmTest(TestCase):
    def test_uninet_hb(self):
        self.assertEqual(get_data_for_uninet_base.get_firm(PATH_BASE_TEST, (150, 183)), {150: 'Uninet USA', 183: 'H&B'})
        self.assertNotEqual(get_data_for_uninet_base.get_firm(PATH_BASE_TEST, (150, 204)), {150: 'Uninet USA', 183: 'H&B'})

    def test_olansi(self):
        self.assertEqual(get_data_for_uninet_base.get_firm(PATH_BASE_TEST, (204,)), {204: 'Olansi'})


class Get_data_from_passTest(TestCase):
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
            get_data_for_uninet_base.get_data_from_pass(PATH_BASE_TEST + 'warehous.dbf', 'KOL_SKL', FILTER_GROUP_KM_HB)[
                'KM1196'], _result)

    def test_goods(self):
        _result = {'cod': 809,
                   'cond_id': 0,
                   'cond_str': '          ',
                   'curr': '   ',
                   'dsn_id': 0,
                   'firm': 183,
                   'group': 'HB',
                   'groupid': 783,
                   'kpr1': 0.0,
                   'kpr2': 0.0,
                   'kpr3': 0.0,
                   'kpr4': 0.0,
                   'kpr5': 0.0,
                   'label_txt': '                              ',
                   'mark': ' ',
                   'min_qty': 0,
                   'model': '476427              ',
                   'model_txt': 'HP CLJ Pro M452/MFP M377/477 Чіп Червоний картріджа 2,3k '
                                'CF413A                                     ',
                   'price_a': 0.0,
                   'price_b': 1.1,
                   'price_bas': 0.0,
                   'price_c': 1.15,
                   'price_d': 1.2,
                   'price_dm': 0.0,
                   'price_opt': 0.0,
                   'price_sale': 1.5,
                   'prod_code': '8443991000  ',
                   'profit': 0,
                   'public_mod': 'Чип Красный картриджа HP CLJ Pro M452/MFP M377/477 2,3k chip '
                                 'Magenta CF413A',
                   'public_txt': '',
                   'show_prg': True,
                   'show_site': True,
                   'size': 0,
                   'tax_ack': 0,
                   'tax_tam': 0,
                   'testico': 1,
                   'url': '',
                   'warranty': 0}
        self.assertEqual(
            get_data_for_uninet_base.get_data_from_pass(PATH_BASE_TEST + 'goods.dbf', 'SHOW_PRG', FILTER_GROUP_KM_HB)[
                'HB809'], _result)


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(get_data_for_uninet_base))
    return tests


if __name__ == '__main__':
    main()
