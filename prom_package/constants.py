import os

HOST = 'my.prom.ua'  # e.g.: my.prom_package.ua, my.tiu.ru, my.satu.kz, my.deal.by, my.prom_package.md

# For skipping tests that hit the real API server.
SKIP_REAL = os.getenv('SKIP_REAL', False)

# Base setting
PATH_BASE_TEST = "..\\tests\\dbf\\"