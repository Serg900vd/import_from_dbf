# Обновление данных для UNINET base.xls
#
import csv
from pathlib import Path
from sys import argv
from typing import List, Tuple, Union

import dbf

# Read the start path
PATH_UNINET = Path(__file__).parent

PATH_BASE = Path("d:/bases/work/pass_base/")
PATH_BASE_TEST = Path("../tests/dbf/")
CODEPAGE = 'cp1251'
FILTR_FIRM_UNINET_KM_HB = (150, 183)
FILTER_GROUP_KM_HB = ('KM', 'HB')


class BasePassDBF:
    def __init__(self, path_base: Path, codepage: str,
                 filter_id_firm: Tuple[int, ...] = None,
                 key_field_warehous: Union[str, int] = 0,
                 key_field_goods: Union[str, int] = 0,
                 filter_group: Tuple[str, ...] = None):
        self.path_base = path_base
        self.codepage = codepage
        self.filter_id_firm = filter_id_firm
        self.key_field_warehous = key_field_warehous
        self.key_field_goods = key_field_goods
        self.filter_group = filter_group
        self.warehous = {}
        self.invoice = {}
        self.goods = {}
        self.firm = {}

    def __repr__(self):
        text = f'{self.__class__.__name__} [path_base= {self.path_base}, codepage: "{self.codepage}", ' \
               f'filter_id_firm: {self.filter_id_firm}, ' \
               f'key_field_warehous: "{self.key_field_warehous}", ' \
               f'key_field_goods: "{self.key_field_goods}",' \
               f'self.filter_group: {self.filter_group}]'
        return text

    def set_firm(self, filter_id_firm: Tuple[int, ...] = None) -> bool:
        """
        Возвращает, из файла firm.dbf, словарь в котором ключ поле FIRM, значение поле FIRM_TXT
        Результат передает в параметр self.firm
        :param filter_id_firm: (150, 183) коды FIRM которые необходимо отфильтровать
        :return: bool
        """
        if not filter_id_firm:
            filter_id_firm = self.filter_id_firm
        _file = self.path_base / 'firm.dbf'
        if not Path.is_file(_file):
            raise FileNotFoundError(f'Нет необходимого файла {_file}')
        _firm = {}
        with dbf.Table(str(_file), codepage=self.codepage) as f:
            with f.open() as ff:
                for row in ff:
                    if row and not dbf.is_deleted(row) and not row.REC_OFF and (
                            not filter_id_firm or row.FIRM in filter_id_firm):
                        _firm[row.FIRM] = row.FIRM_TXT.strip()
        self.firm = _firm
        return bool(_firm)

    @classmethod
    def get_data_from_pass(cls, file_name: Path, codepage: str, key_tabl=lambda row: row.GROUP + str(row.COD) + row.INV,
                           key_field: Union[str, int] = 0,
                           filter_group: tuple = None) -> dict:
        """
        Возвращает словарь по ключу key_tabl с вложенными строками в виде словаря {поле : значение ...}
        :param file_name: path + file_name.dbf
        :param codepage: 'cp1251'
        :param key_tabl: lambda row: row.GROUP + str(row.COD) + row.INV (ключ таблицы по умолчанию)
        :param key_field: 'SHOW_PRG' Имя поля или индекс. Значение True включает строку в результат
        :param filter_group: ('KM', 'HB') кортеж с значениями поля GROUP которые необходимо отфильтровать
        :return: {key_tabl : {'group': 'KM', 'cod': 750, 'groupid': 695, ...(все поля таблицы)}, ...}
        """
        if not file_name.is_file():
            raise FileNotFoundError(f'Нет необходимого файла {file_name}')
        result = {}
        with dbf.Table(str(file_name), codepage=codepage) as f:
            with f.open() as ff:
                field_names = ff.field_names
                for row in ff:
                    if row and not dbf.is_deleted(row) and row[key_field] and (
                            not filter_group or row.GROUP in filter_group):
                        feilds = {}
                        for j, feild in enumerate(row):
                            feilds[field_names[j].lower()] = feild
                        result[key_tabl(row)] = feilds
        return result

    def load_tables_dbf(self):
        print(str(self))

        self.warehous = self.get_data_from_pass(self.path_base / 'warehous.dbf', self.codepage,
                                                key_field=self.key_field_warehous,
                                                filter_group=self.filter_group)
        print('warehous loaded')

        self.invoice = self.get_data_from_pass(self.path_base / 'invoice.DBF', self.codepage,
                                               key_tabl=lambda row: row.INV)
        print('invoice loaded')

        self.goods = self.get_data_from_pass(self.path_base / 'goods.dbf', self.codepage,
                                             key_tabl=lambda row: row.GROUP + str(row.COD),
                                             key_field=self.key_field_goods,
                                             filter_group=self.filter_group)
        print('goods loaded')

        self.set_firm()
        print('firm loaded')

    def get_warehous_grcod_filter(self, group_cod: str) -> List[dict]:
        """
        Получаем список всех строк (приходы) для заданного продукта (уникальный ключ 'group_cod') из таблицы warehous
        :param group_cod:
        :return:
        """
        return [row for row in self.warehous.values() if row['group'] + str(row['cod']) == group_cod]

    def get_warehous_grcod_sum(self, group_cod: str) -> dict:
        """
        Суммируем приходы для заданного продукта
        :param group_cod:
        :return:
        """
        _group_cod_list = self.get_warehous_grcod_filter(group_cod)

        _group_cod_sum = {'group_cod': group_cod, 'kol': 0, 'kol_otkaz': 0, 'kol_rezerv': 0, 'kol_sale': 0,
                          'kol_sf': 0, 'kol_skl': 0, 'old_sale': 0}
        _parameters = list(_group_cod_sum.keys())
        _parameters.remove('group_cod')

        for row in _group_cod_list:
            for param in _parameters:
                _group_cod_sum[param] += row[param]
        return _group_cod_sum

    def is_product_on_stock(self, group_cod: str) -> bool:
        """
        В наличие на складе?
        :param group_cod:
        :return:
        """
        product = self.get_warehous_grcod_sum(group_cod)
        return product['kol_skl'] - product['kol_rezerv'] > 0


def main_uninet(path: Union[Path, None], file_name_out: str, paht_out: Path = None):
    """
    Формируем финальную таблицу для выдачи.
    :param path: путь к базе
    :param file_name_out: имя файла с результатом в формате .csv
    :param paht_out: путь файла результата
    """
    if not paht_out:
        paht_out = path

    # Быстрое решение через функцию load_tables_dbf_uninet()
    # Загружаем таблицы
    # warehous, invoice, goods = load_tables_dbf_uninet(path)
    # firm = {150: 'Uninet USA', 183: 'H&B'}

    # Initialize Base Data for Uninet
    bd = BasePassDBF(path, CODEPAGE, FILTR_FIRM_UNINET_KM_HB, 'KOL_SKL', 0, FILTER_GROUP_KM_HB)
    # Load tables
    bd.load_tables_dbf()
    warehous, invoice, goods, firm = bd.warehous, bd.invoice, bd.goods, bd.firm

    uninet = []
    header = [('товарная_группа', 'код_товара', 'код_прихода', 'накладная', 'дата', 'поставщик', 'модель',
               'наименование', 'фирма', 'приход', 'склад', 'свободно', 'резерв', 'выписано', 'оплачено', 'usd_закупка',
               'грн_закупка', 'usd_a', 'usd_b', 'usd_c', 'usd_d', 'usd_розница')]
    # count = 0
    for group_cod_inv, row in warehous.items():
        inv = row['inv']
        group_cod = row['group'] + str(row['cod'])
        row_out = (row['group'],
                   row['cod'],
                   inv,
                   invoice[inv]['inv_txt'].strip(),
                   invoice[inv]['inv_day'].strftime('%d.%m.%Y'),
                   invoice[inv]['cust'],
                   goods[group_cod]['model'].strip(),
                   goods[group_cod]['model_txt'].strip(),
                   firm[goods[group_cod]['firm']],
                   warehous[group_cod_inv]['kol'],
                   warehous[group_cod_inv]['kol_skl'],
                   warehous[group_cod_inv]['kol_skl']
                        - warehous[group_cod_inv]['kol_rezerv']
                        - warehous[group_cod_inv]['kol_otkaz'],
                   warehous[group_cod_inv]['kol_rezerv'],
                   warehous[group_cod_inv]['kol_sf'],
                   warehous[group_cod_inv]['kol_sale'],
                   warehous[group_cod_inv]['price_usd'],
                   warehous[group_cod_inv]['price_krb'],
                   goods[group_cod]['price_a'],
                   goods[group_cod]['price_b'],
                   goods[group_cod]['price_c'],
                   goods[group_cod]['price_d'],
                   goods[group_cod]['price_sale'],
                   )
        uninet.append(row_out)
        # if count > 4: break
        # count += 1

    uninet.sort(key=lambda j: (j[0], j[1]))
    uninet = header + uninet

    if not Path.is_dir(paht_out):
        raise FileNotFoundError(f'Нет такого пути {paht_out}')

    with open(paht_out / file_name_out, 'w') as f:
        ff = csv.writer(f, delimiter=',', lineterminator='\n')
        for row in uninet:
            ff.writerow(row)
    print(f'Результат записан в {paht_out / file_name_out}')


def main():
    # Для создания .exe запустить:
    # pyinstaller get_data_uninet.py --onefile
    path_base = path_result = PATH_BASE_TEST
    argvlen = len(argv)
    if argvlen == 2:
        path_base = path_result = Path(argv[1])
    elif argvlen == 3:
        path_base, path_result = Path(argv[1]), Path(argv[2])

    print('Путь к базе ', path_base)
    main_uninet(path_base, 'stock_uninet.csv', path_result)


if __name__ == '__main__':
    main()

    # main_uninet(PATH_BASE, 'stock_uninet.csv')
    #
