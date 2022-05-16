# Обновление данных для UNINET base.xls
#
import csv
import os
from sys import argv

import dbf

PATH_BASE = "d:\\Kotik\\work\\2012_toner_base\\"
PATH_BASE_TEST = "..\\tests\\dbf\\"
CODEPAGE = 'cp1251'
FILTR_FIRM_UNINET_KM_HB = (150, 183)
FILTER_GROUP_KM_HB = ('KM', 'HB')


class BasePassDBF:
    def __init__(self, path_base, codepage, filter_id_firm=None, key_field_warehous=0, filter_group: tuple = None):
        self.path_base = path_base
        self.codepage = codepage
        self.filter_id_firm = filter_id_firm
        self.key_field_warehous = key_field_warehous
        self.filter_group = filter_group
        self.warehous = {}
        self.invoice = {}
        self.goods = {}
        self.firm = {}

    def __repr__(self):
        text = f'Parameters [path_base= {self.path_base}, codepage: "{self.codepage}", ' \
               f'filter_id_firm: {self.filter_id_firm}, key_field_warehous: "{self.key_field_warehous}", ' \
               f'self.filter_group: {self.filter_group}]'
        return text

    def set_firm(self, filter_id_firm=None) -> bool:
        """
        Возвращает, из файла firm.dbf, словарь в котором ключ поле FIRM, значение поле FIRM_TXT
        Результат передает в параметр self.firm
        :param filter_id_firm: (150, 183) коды FIRM которые необходимо отфильтровать
        :return: bool
        """
        if not filter_id_firm:
            filter_id_firm = self.filter_id_firm
        _file = self.path_base + 'firm.dbf'
        if not os.path.isfile(_file):
            raise FileNotFoundError(f'Нет необходимого файла {_file}')
        _firm = {}
        f = dbf.Table(_file, codepage=self.codepage)
        with f.open() as ff:
            for row in ff:
                if row and not dbf.is_deleted(row) and not row.REC_OFF and (
                        not filter_id_firm or row.FIRM in filter_id_firm):
                    _firm[row.FIRM] = row.FIRM_TXT.strip()
        self.firm = _firm
        return bool(_firm)

    @classmethod
    def get_data_from_pass(cls, file_name: str, codepage: str, key_tabl=lambda row: row.GROUP + str(row.COD) + row.INV,
                           key_field: str = 0,
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
        if not os.path.isfile(file_name):
            raise FileNotFoundError(f'Нет необходимого файла {file_name}')
        result = {}
        f = dbf.Table(file_name, codepage=codepage)
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

        self.warehous = self.get_data_from_pass(self.path_base + 'warehous.dbf', self.codepage,
                                                key_field=self.key_field_warehous,
                                                filter_group=self.filter_group)
        print('warehous loaded')

        self.invoice = self.get_data_from_pass(self.path_base + 'invoice.DBF', self.codepage, lambda row: row.INV)
        print('invoice loaded')

        self.goods = self.get_data_from_pass(self.path_base + 'goods.dbf', self.codepage,
                                             key_tabl=lambda row: row.GROUP + str(row.COD),
                                             key_field='SHOW_PRG', filter_group=self.filter_group)
        print('goods loaded')

        self.set_firm()
        print('firm loaded')

    def get_warehous_grcod_filter(self, group_cod):
        return [row for row in self.warehous.values() if row['group'] + str(row['cod']) == group_cod]

    def get_warehous_grcod_sum(self, group_cod):
        _group_cod_list = self.get_warehous_grcod_filter(group_cod)

        _parameters = ['kol', 'kol_otkaz', 'kol_rezerv', 'kol_sale', 'kol_sf', 'kol_skl', 'old_sale']
        _group_cod_sum = {'group_cod': group_cod, 'kol': 0, 'kol_otkaz': 0, 'kol_rezerv': 0, 'kol_sale': 0,
                         'kol_sf': 0, 'kol_skl': 0, 'old_sale': 0}

        for row in _group_cod_list:
            for param in _parameters:
                _group_cod_sum[param] += row[param]
        return _group_cod_sum


def load_tables_dbf_uninet(path: str):
    warehous = BasePassDBF.get_data_from_pass(path + 'warehous.dbf', CODEPAGE, key_field='KOL_SKL',
                                              filter_group=FILTER_GROUP_KM_HB)
    print('warehous loaded')

    invoice = BasePassDBF.get_data_from_pass(path + 'invoice.DBF', CODEPAGE, lambda row: row.INV)
    print('invoice loaded')

    goods = BasePassDBF.get_data_from_pass(path + 'goods.dbf', CODEPAGE, key_tabl=lambda row: row.GROUP + str(row.COD),
                                           key_field='SHOW_PRG',
                                           filter_group=FILTER_GROUP_KM_HB)
    print('goods loaded')

    return warehous, invoice, goods


def main_uninet(path: str, file_name_out: str, paht_out: str = None):
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
    bd = BasePassDBF(path, CODEPAGE, FILTR_FIRM_UNINET_KM_HB, 'KOL_SKL', FILTER_GROUP_KM_HB)
    # Load tables
    bd.load_tables_dbf()
    warehous, invoice, goods, firm = bd.warehous, bd.invoice, bd.goods, bd.firm

    uninet = []
    header = [('товарная_группа', 'код_товара', 'код_прихода', 'накладная', 'дата', 'поставщик', 'модель',
               'наименование', 'фирма', 'приход', 'склад', 'свободно', 'резерв', 'выписано', 'оплачено', 'usd_закупка',
               'грн_закупка', 'usd_a', 'usd_b', 'usd_c', 'usd_d', 'usd_розница')]
    count = 0
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
                   warehous[group_cod_inv]['kol_skl'] - warehous[group_cod_inv]['kol_rezerv'],
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

    if not os.path.isdir(paht_out):
        raise FileNotFoundError(f'Нет такого пути {paht_out}')

    with open(paht_out + file_name_out, 'w') as f:
        ff = csv.writer(f, delimiter=',', lineterminator='\n')
        for row in uninet:
            ff.writerow(row)
    print(f'Результат записан в {paht_out + file_name_out}')


def cut_tabl(file_name, namber_row):
    """
    Обрезка файлов для тестов
        # cut_tabl('invoice.DBF', 13600)
    :param file_name:
    :param namber_row: номер строки по которую обрезаем
    :return:
    """
    if not os.path.isfile(PATH_BASE + file_name):
        raise FileNotFoundError(f'Нет необходимого файла {PATH_BASE + file_name}')
    f = dbf.Table(PATH_BASE + file_name, codepage=CODEPAGE)
    with f.open() as ff:
        g = ff.new(PATH_BASE_TEST + file_name)
        with g.open(mode=dbf.READ_WRITE) as gg:
            for j, row in enumerate(ff):
                if j > namber_row:
                    gg.append(row)
    print(f'В файле {file_name} записи с 0 по {namber_row} удалены. \n Результат в дирректории {PATH_BASE_TEST}')


def creat_tabl_related_master(file_name_master: str, file_name_slave: str, key_tabl,
                              key_tabl_master=lambda row: row.GROUP + str(row.COD) + row.INV):
    """
        Создание файла file_name_slave cо всеми записями с зависимостями от file_name_master
        Для тестов
    Путь источник PATH_BASE для исходного файла file_name_slave
    Путь результата PATH_BASE_TEST
        # creat_tabl_related_master('warehous.DBF', 'invoice.DBF', lambda row: row['inv'])
        # creat_tabl_related_master('warehous.DBF', 'goods.DBF', lambda row: row['group'] + str(row['cod']))
        # creat_tabl_related_master('goods.DBF','firm.DBF', lambda row: row['firm'],
        # lambda row: row.GROUP + str(row.COD))
    :param file_name_master: Имя файла таблицы master
    :param file_name_slave: Имя файла таблицы slave
    :param key_tabl: lambda row: row['inv'] Функция ключа для таблицы slave
    :param key_tabl_master: lambda row: row['group'] + str(row['cod']) + row['inv'] Функция ключа для таблицы master
    :return:
    """
    master = BasePassDBF.get_data_from_pass(PATH_BASE_TEST + file_name_master, CODEPAGE, key_tabl=key_tabl_master)
    master_keys = set(key_tabl(row) for row in master.values())
    # master_keys = {2, 183, 12, 7, 41, 39, 204, 9, 150, 50}  # all firms
    # print(master_keys)

    if not os.path.isfile(PATH_BASE + file_name_slave):
        raise FileNotFoundError(f'Нет необходимого файла {PATH_BASE + file_name_slave}')

    f = dbf.Table(PATH_BASE + file_name_slave, codepage=CODEPAGE)
    with f.open() as ff:
        g = ff.new(PATH_BASE_TEST + file_name_slave)
        with g.open(mode=dbf.READ_WRITE) as gg:
            print(gg.field_names)
            for row in ff:
                if key_tabl(row) in master_keys:
                    gg.append(row)
                    # print(row)
                    # print('-' * 30)

    print(f'Результат в {PATH_BASE_TEST} {file_name_slave}')


def main():
    # Для создания .exe запустить:
    # pyinstaller get_data_uninet.py --onefile

    argvlen = len(argv)
    if argvlen == 1:
        path_base = path_result = PATH_BASE_TEST
    elif argvlen == 2:
        path_base = path_result = argv[1]
    elif argvlen == 3:
        path_base, path_result = argv[1], argv[2]

    # path_base, path_result = argv[1], argv[2]
    print('Путь к базе ', path_base)
    main_uninet(path_base, 'stock_uninet.csv', path_result)


if __name__ == '__main__':
    main()

    # main_uninet(PATH_BASE, 'stock_uninet.csv')
    #
    # invoice = get_data_from_pass(PATH_BASE_TEST + 'firm.DBF', lambda row: row.FIRM, 'REC_OFF')
    # print(invoice)

    # invoice = get_data_from_pass(PATH_BASE_TEST + 'invoice.DBF', lambda row: row.INV)
    # print(invoice['DBE8'])
    #
    # goods = get_data_from_pass(PATH_BASE_TEST + 'goods.dbf', key_field='SHOW_PRG', filter_group=FILTER_GROUP_KM_HB)
    # print(goods['HB812'])  # ['HB812']
    #
    # warehous = get_data_from_pass(PATH_BASE_TEST + 'warehous.dbf',)
    # key_field='KOL_SKL',
    # filter_group=FILTER_GROUP_KM_HB)
    # print(warehous)  # ['KM1196']
