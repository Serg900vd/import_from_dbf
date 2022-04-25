from unittest import TestCase, main
import doctest
from work import get_data_for_uninet_base

PATH_BASE = "\\dbf\\"
CODEPAGE = 'cp1251'
FILTR_FIRM_UNINET_HB = (150, 183)
FILTER_GROUP_KM_HB = ('KM', 'HB')


class Get_firmTest(TestCase):
    def test_uninet_hb(self):
        self.assertEqual(get_data_for_uninet_base.get_firm((150, 183)), {150: 'Uninet USA', 183: 'H&B'})
        self.assertNotEqual(get_data_for_uninet_base.get_firm((150, 204)), {150: 'Uninet USA', 183: 'H&B'})

    def test_olansi(self):
        self.assertEqual(get_data_for_uninet_base.get_firm((204,)), {204: 'Olansi'})


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(get_data_for_uninet_base))
    return tests


if __name__ == '__main__':
    main()
