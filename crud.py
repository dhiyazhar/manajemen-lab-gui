from abc import ABC, abstractmethod

class CRUD(ABC):
    def __init__(self, file_path):
        self.file_path = file_path

    @abstractmethod
    def add_data(self, data):
        pass

    @abstractmethod
    def delete_data(self, data): 
        pass

    @abstractmethod
    def edit_data(self, data, data_baru):
        pass

    def load_data(self, data):
        pass
