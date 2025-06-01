from abc import ABC, abstractmethod

class UtilizadorInterface(ABC):

    @abstractmethod
    def criar_user(self, collection) -> bool:
        pass



