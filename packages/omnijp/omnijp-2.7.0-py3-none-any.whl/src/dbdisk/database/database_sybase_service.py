from src.dbdisk.database.database_service import DatabaseService


class DatabaseSybaseService(DatabaseService):
    def __init__(self, connection_string):
        super().__init__(connection_string)

    def connect(self):
        import pymssql
        return pymssql.connect(self.connection_string)

