# Service auxiliary functions
from pathlib import Path

import dbf

from uninet.get_data_uninet import BasePassDBF, CODEPAGE, FILTER_GROUP_KM_HB, PATH_BASE, PATH_BASE_TEST


def load_tables_dbf_uninet(path: Path):
    warehous = BasePassDBF.get_data_from_pass(path / 'warehous.dbf', CODEPAGE, key_field='KOL_SKL',
                                              filter_group=FILTER_GROUP_KM_HB)
    print('warehous loaded')

    invoice = BasePassDBF.get_data_from_pass(path / 'invoice.DBF', CODEPAGE, key_tabl=lambda row: row.INV)
    print('invoice loaded')

    goods = BasePassDBF.get_data_from_pass(path / 'goods.dbf', CODEPAGE, key_tabl=lambda row: row.GROUP + str(row.COD),
                                           key_field='SHOW_PRG',
                                           filter_group=FILTER_GROUP_KM_HB)
    print('goods loaded')

    return warehous, invoice, goods


def cut_tabl(file_name: Path, namber_row: int):
    """
    Обрезка файлов для тестов
        # cut_tabl('invoice.DBF', 13600)
    :param file_name:
    :param namber_row: номер строки по которую обрезаем
    :return:
    """
    if not Path.is_file(PATH_BASE / file_name):
        raise FileNotFoundError(f'Нет необходимого файла {PATH_BASE / file_name}')
    f = dbf.Table(PATH_BASE / file_name, codepage=CODEPAGE)
    with f.open() as ff:
        g = ff.new(PATH_BASE_TEST / file_name)
        with g.open(mode=dbf.READ_WRITE) as gg:
            for j, row in enumerate(ff):
                if j > namber_row:
                    gg.append(row)
    print(f'В файле {file_name} записи с 0 по {namber_row} удалены. \n Результат в дирректории {PATH_BASE_TEST}')


def creat_tabl_related_master(file_name_master: Path, file_name_slave: Path, key_tabl,
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
    master = BasePassDBF.get_data_from_pass(PATH_BASE_TEST / file_name_master, CODEPAGE, key_tabl=key_tabl_master)
    master_keys = set(key_tabl(row) for row in master.values())
    # master_keys = {2, 183, 12, 7, 41, 39, 204, 9, 150, 50}  # all firms
    # print(master_keys)

    if not Path.is_file(PATH_BASE / file_name_slave):
        raise FileNotFoundError(f'Нет необходимого файла {PATH_BASE / file_name_slave}')

    f = dbf.Table(PATH_BASE / file_name_slave, codepage=CODEPAGE)
    with f.open() as ff:
        g = ff.new(PATH_BASE_TEST / file_name_slave)
        with g.open(mode=dbf.READ_WRITE) as gg:
            print(gg.field_names)
            for row in ff:
                if key_tabl(row) in master_keys:
                    gg.append(row)
                    # print(row)
                    # print('-' * 30)

    print(f'Результат в {PATH_BASE_TEST} {file_name_slave}')


if __name__ == '__main__':
    pass
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
