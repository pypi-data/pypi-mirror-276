import pymssql

from src.dbdisk.database.database_service import DatabaseService


class DatabaseSybaseService(DatabaseService):
    def __init__(self, connection_string):
        super().__init__(connection_string)

    def execute(self, query):
        try:
            connection = pymssql.connect(self.connection_string)
            cursor = connection.cursor()
            cursor.execute(query)

        except pymssql.Error as e:
            print("Error connecting to Sybase:", e)

        finally:
            header = [desc[0] for desc in cursor.description]
            return header, cursor.fetchall()
            if cursor:
                cursor.close()
            if connection:
                connection.close()
