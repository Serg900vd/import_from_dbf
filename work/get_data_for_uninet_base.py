# Обновление данных для UNINET base.xls
#
from typing import Tuple

PATH_BASE = "d:\\Kotik\\work\\2012_toner_base\\"
CODEPAGE = 'cp1251'
FILTR_FIRM_UNINET_HB =(150, 183)

import dbf


def get_warehous() -> list:
    warehous = []
    f = dbf.Table(PATH_BASE + 'warehous.dbf', codepage=CODEPAGE)
    with f.open() as ff:
        aa = ff.field_names
        row_out = ('inv', 'group_cod', 'group', 'cod', 'price_usd', 'kol', 'kol_skl', 'kol_rezerv', 'kol_sf')
        warehous.append(row_out)
        for row in ff:
            if row and not dbf.is_deleted(row) and row.KOL_SKL:
                row_out = (
                    row.INV, row.GROUP + str(row.COD), row.GROUP, row.COD, row.PRICE_USD, row.KOL, row.KOL_SKL,
                    row.KOL_REZERV,
                    row.KOL_SF)
                warehous.append(row_out)
    return warehous


def get_firm(filter_id_firm: tuple = None) -> dict:
    firm = {}
    f = dbf.Table(PATH_BASE + 'firm.dbf', codepage=CODEPAGE)
    with f.open() as ff:
        for row in ff:
            if row and not dbf.is_deleted(row) and not row.REC_OFF and (
                    not filter_id_firm or row.FIRM in filter_id_firm):
                firm[row.FIRM] = row.FIRM_TXT.strip()
    return firm


def get_goods():
    goods = []
    f = dbf.Table(PATH_BASE + 'goods.DBF', codepage=CODEPAGE)
    with f.open() as ff:
        aa = ff.field_names
        row_out = ('inv')
        goods.append(row_out)
        for row in ff:
            if row and not dbf.is_deleted(row) and row.QTY:
                row_out = (
                    row.INV, row.GROUP + str(row.COD), row.GROUP, row.COD, row.PRICE_USD, row.KOL, row.KOL_SKL,
                    row.KOL_REZERV,
                    row.KOL_SF)
                goods.append(row_out)

    pass


if __name__ == '__main__':
    firm = get_firm((150, 183))  # (Uninet USA, H&B)
    assert (get_firm((150, 183)) == {150: 'Uninet USA', 183: 'H&B'}), "{150: 'Uninet USA', 183: 'H&B'}"

    warehous = get_warehous()

    catalogue = get_goods()
    print(catalogue)
    pass
