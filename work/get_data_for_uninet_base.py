# Обновление данных для UNINET base.xls
#
from typing import Tuple

PATH_BASE = "d:\\Kotik\\work\\2012_toner_base\\"
CODEPAGE = 'cp1251'
FILTR_FIRM_UNINET_HB = (150, 183)
FILTER_GROUP_KM_HB = ('KM', 'HB')

import dbf


def get_firm(filter_id_firm: tuple = None) -> dict:
    """
    Возвращает, из файла firm.dbf, словарь в котором ключ поле FIRM, значение поле FIRM_TXT
    :param filter_id_firm:
    :return: dict
    >>> get_firm((150, 183))
    {150: 'Uninet USA', 183: 'H&B'}
    >>> get_firm((150, ))
    {150: 'Uninet USA'}
    """
    firm = {}
    f = dbf.Table(PATH_BASE + 'firm.dbf', codepage=CODEPAGE)
    with f.open() as ff:
        for row in ff:
            if row and not dbf.is_deleted(row) and not row.REC_OFF and (
                    not filter_id_firm or row.FIRM in filter_id_firm):
                firm[row.FIRM] = row.FIRM_TXT.strip()
    return firm


def get_data_from_pass(file_name: str, key_field: str = 0, filter_group: tuple = None) -> dict:
    """
    Возвращает словарь в словаре по ключу groupcod
    :param file_name: pass + file_name.dbf
    :param key_field: 'SHOW_PRG' Имя поля или индекс. Значение True включает строку в результат
    :param filter_group: ('KM', 'HB') кортеж с значениями поля GROUP которые необходимо отфильтровать
    :return: {'KM750'- gropcod : {'group': 'KM', 'cod': 750, 'groupid': 695, ...(все поля таблицы)}}
    """
    data = {}
    f = dbf.Table(file_name, codepage=CODEPAGE)
    with f.open() as ff:
        field_names = ff.field_names
        for row in ff:
            if row and not dbf.is_deleted(row) and row[key_field] and (not filter_group or row.GROUP in filter_group):
                group_cod_feilds = {}
                for j, feild in enumerate(row):
                    group_cod_feilds[field_names[j].lower()] = feild
                data[row.GROUP + str(row.COD)] = group_cod_feilds
    return data


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    goods = get_data_from_pass(PATH_BASE + 'goods.dbf', 'SHOW_PRG', FILTER_GROUP_KM_HB)
    print(goods['KM750'])

    warehous = get_data_from_pass(PATH_BASE + 'warehous.dbf', 'KOL_SKL', FILTER_GROUP_KM_HB)
    print(warehous['KM750'])

    # warehous = get_warehous(FILTER_GROUP_KM_HB)
    # print(len(warehous))
    #
    # firm = get_firm((151, 183))  # (Uninet USA, H&B)
    # print(firm)
    # assert (get_firm((150, 183)) == {150: 'Uninet USA', 183: 'H&B'}), "{150: 'Uninet USA', 183: 'H&B'}"

    pass
