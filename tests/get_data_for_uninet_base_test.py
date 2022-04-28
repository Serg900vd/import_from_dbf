from unittest import TestCase, main
import os, datetime
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
        self.assertNotEqual(get_data_for_uninet_base.get_firm(PATH_BASE_TEST, (150, 204)),
                            {150: 'Uninet USA', 183: 'H&B'})

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
            get_data_for_uninet_base.get_data_from_pass(PATH_BASE_TEST + 'warehous.dbf', key_field='KOL_SKL',
                                                        filter_group=FILTER_GROUP_KM_HB)[
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
            get_data_for_uninet_base.get_data_from_pass(PATH_BASE_TEST + 'goods.dbf', key_field='SHOW_PRG',
                                                        filter_group=FILTER_GROUP_KM_HB)[
                'HB809'], _result)

    def test_invoice(self):
        _result = {'app_num': 0,
                   'auto_id': 0,
                   'cond': 2,
                   'condition': 'ПРОДАЖИ   ',
                   'contract': '                    ',
                   'curr': '001',
                   'cust': 1377,
                   'dm_usd': 1.0,
                   'inv': 'DBE8',
                   'inv_day': datetime.date(2021, 7, 6),
                   'inv_nkl': 483895,
                   'inv_reg': datetime.date(2021, 7, 6),
                   'inv_txt': 'лидер сч 268                                      ',
                   'krb_usd': 1.0,
                   'notes': '',
                   'peo': 0,
                   'sum_inv': 6277477.43,
                   'sum_krb': 45008310.02,
                   'sum_usd': 16872163.69,
                   'taking_day': None,
                   'tax_nds': 1,
                   'tax_proc': 1.0,
                   'tax_tam': 0,
                   'user_id': 22}
        self.assertEqual(
            get_data_for_uninet_base.get_data_from_pass(PATH_BASE_TEST + 'invoice.DBF', lambda row: row.INV)[
                'DBE8'], _result)


if __name__ == '__main__':
    main()
