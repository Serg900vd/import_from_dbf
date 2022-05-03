#
# main_get_uninet.py d:\Kotik\work\2012_toner_base\ d:\Kotik\work\
import work.get_data_for_uninet_base as wu
from sys import argv

# argvlen = len(argv)
# if argvlen == 1:
#     path_base = path_result = 'tests\\dbf\\'
# elif argvlen == 2:
#     path_base = path_result = argv[1]
# elif argvlen == 3:
#     path_base, path_result = argv[1], argv[2]
path_base, path_result = argv[1], argv[2]

wu.main_uninet(path_base, 'stock_uninet.csv', path_result)
