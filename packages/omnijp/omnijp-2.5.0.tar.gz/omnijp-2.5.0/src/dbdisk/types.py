from enum import Enum


class DiskFileType(Enum):
    CSV = '.csv'
    TXT = '.txt'


class DbType(Enum):
    NONE = 1
    POSTGRESQL = 2
    SYBASE = 3