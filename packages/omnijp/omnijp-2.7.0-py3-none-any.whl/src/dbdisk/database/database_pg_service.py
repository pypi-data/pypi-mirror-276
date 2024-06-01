from src.dbdisk.database.database_service import DatabaseService


class DatabasePgService(DatabaseService):
    def __init__(self, connection_string):
        super().__init__(connection_string)

    def connect(self):
        import psycopg2
        return psycopg2.connect(self.connection_string)

