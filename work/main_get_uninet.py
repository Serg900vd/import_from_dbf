#
# main_get_uninet.py d:\Kotik\work\2012_toner_base\ d:\Kotik\work\
import get_data_for_uninet_base
from sys import argv

argvlen = len(argv)
if argvlen == 1:
    path_base = path_result = get_data_for_uninet_base.PATH_BASE_TEST
elif argvlen == 2:
    path_base = path_result = argv[1]
elif argvlen == 3:
    path_base, path_result = argv[1], argv[2]

get_data_for_uninet_base.main_uninet(path_base, 'stock_uninet.csv', path_result)
