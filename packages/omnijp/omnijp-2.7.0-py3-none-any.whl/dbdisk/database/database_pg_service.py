import psycopg2

from src.dbdisk.database.database_service import DatabaseService


class DatabasePgService(DatabaseService):
    def __init__(self, connection_string):
        super().__init__(connection_string)

    def execute(self, query):
        try:
            connection = psycopg2.connect(self.connection_string)
            cursor = connection.cursor()
            cursor.execute(query)

        except psycopg2.Error as e:
            print("Error connecting to PostgresSQL:", e)

        finally:
            header = [desc[0] for desc in cursor.description]
            return header, cursor.fetchall()
            if cursor:
                cursor.close()
            if connection:
                connection.close()
