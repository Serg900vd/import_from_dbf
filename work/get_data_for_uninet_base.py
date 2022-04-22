# Обновление данных для UNINET base.xls
#
PATH_BASE = "d:\\Kotik\\work\\2012_toner_base\\"

import dbf


def get_warehous(PATH_BASE)->list:
    warehous = []
    f = dbf.Table(PATH_BASE + 'warehous.dbf', codepage='cp866')
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


def get_firm(PATH_BASE)-> dict:
    firm = {}
    f = dbf.Table(PATH_BASE + 'firm.dbf', codepage='cp866')
    with f.open() as ff:
        for row in ff:
            if row and not dbf.is_deleted(row) and not row.REC_OFF:
                firm[row.FIRM] = row.FIRM_TXT.strip()
    return firm


if __name__ == '__main__':
    # warehous = get_warehous(PATH_BASE)
    firm = get_firm(PATH_BASE)
    print(firm)
    pass
