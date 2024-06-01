from abc import abstractmethod

import psycopg2
import pymssql


class DatabaseService:

    def __init__(self, connection_string):
        self.connection_string = connection_string

    def execute(self, query):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute(query)
            header = [desc[0] for desc in cursor.description]
            result = cursor.fetchall()
        except Exception as e:
            self.handle_error(e)
            result = None
            header = None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        return header, result

    @abstractmethod
    def connect(self):
        pass

    @staticmethod
    def handle_error(error):
        error_messages = {
            psycopg2.Error: "Error connecting to PostgresSQL:",
            pymssql.Error: "Error connecting to Sybase:"
        }
        error_type = type(error)
        message = error_messages.get(error_type, "Unknown error")
        raise Exception(message, error)
