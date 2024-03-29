# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
import logging
import sys
from logging.handlers import RotatingFileHandler

LOG_FILE_MAX_SIZE = 1024 * 1024 * 1024
LOG_FILE_MAX_BACKUP_COUNT = 5

logger = logging.getLogger('common')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[pid:%(process)d]'
                              '[%(levelname)+8s]'
                              '[%(asctime)s]'
                              '[%(module)s]'
                              '[%(funcName)s:%(lineno)d] %(message)s',
                              '%d.%m.%Y %H:%M:%S')

console_handler = logging.StreamHandler(sys.stderr)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


file_handler = RotatingFileHandler(filename='log/autotest.log',
                                   maxBytes=LOG_FILE_MAX_SIZE,
                                   backupCount=LOG_FILE_MAX_BACKUP_COUNT,
                                   encoding='utf-8',
                                   mode='w')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
