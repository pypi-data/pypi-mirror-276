from src.dbdisk import DbDiskRequest
from src.dbdisk.types import DbType, DiskFileType

MAX_ROWS = 1000000
class DbDiskCacheBuilder:
    def __init__(self):
        self.db_type = DbType.NONE
        self.disk_file_type = DiskFileType.CSV
        self.cache_path = None
        self.cache_name = None
        self.connection_string = None
        self.can_zip = False
        self.rows_per_file = MAX_ROWS


    @classmethod
    def create(cls, setup):
        builder = cls()
        setup(builder)
        return builder

    def set_db_type(self, db_type: DbType):
        self.db_type = db_type
        return self
    def set_disk_file_type(self, disk_file_type: DiskFileType):
        self.disk_file_type = disk_file_type
        return self
    def set_cache_path(self, path):
        self.cache_path = path
        return self

    def set_cache_name(self, name):
        self.cache_name = name
        return self

    def set_connection_string(self, connection_string):
        self.connection_string = connection_string
        return self

    def set_can_zip(self, can_zip):
        self.can_zip = can_zip
        return self

    def set_rows_per_file(self, rows_per_file):
        self.rows_per_file = rows_per_file
        return self


    def execute(self, query):
        print(f"Executing query: {query}")
        print(f"Using cache path: {self.cache_path}")
        print(f"Cache name: {self.cache_name}")
        print(f"Connection string: {self.connection_string}")
        print(f"Database type: {self.db_type}")
        return DbDiskRequest(self.connection_string, self.cache_path, self.cache_name,self.disk_file_type, self.can_zip, self.rows_per_file).execute(query)
        # Add actual database execution logic here

