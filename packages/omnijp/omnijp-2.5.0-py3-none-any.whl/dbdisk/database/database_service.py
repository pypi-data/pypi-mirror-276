from abc import abstractmethod


class DatabaseService:

    def __init__(self, connection_string):
       self.connection_string = connection_string

    @abstractmethod
    def execute(self, query):
        pass

