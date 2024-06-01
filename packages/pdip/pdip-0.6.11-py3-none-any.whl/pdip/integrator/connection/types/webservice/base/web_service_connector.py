from abc import abstractmethod

from ......dependency import IScoped


class WebServiceConnector(IScoped):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def get_connection(self):
        pass

    @abstractmethod
    def execute_many(self, query, data):
        pass

    @abstractmethod
    def get_target_query_indexer(self):
        pass

    @abstractmethod
    def prepare_data(self, data):
        return data
