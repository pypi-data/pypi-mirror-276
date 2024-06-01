from src.dbdisk.database.database_pg_service import DatabasePgService
from src.dbdisk.database.database_service import DatabaseService
from src.dbdisk import DbDiskFactory
from src.dbdisk.types import DiskFileType


class DbDiskRequest:
    def __init__(self, connection_string, cache_dir, cache_name, file_type=DiskFileType.CSV, can_zip=False, rows_per_file=1000000):
        self.connection_string = connection_string
        self.cache_dir = cache_dir
        self.cache_name = cache_name
        self.db_service = DatabaseService(connection_string)
        self.file_type = file_type
        self.can_zip = can_zip
        self.rows_per_file = rows_per_file

    def execute(self, query):
        db_pg_service = DatabasePgService(self.connection_string)
        header, data = db_pg_service.execute(query)
        print(data)
        return DbDiskFactory.create_db_disk(self.file_type, self.cache_dir, self.cache_name, self.can_zip, self.rows_per_file).save(header, data)
