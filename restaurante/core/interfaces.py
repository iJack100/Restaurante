from abc import ABC, abstractmethod


class ICrud(ABC):

    @abstractmethod
    def crear(self):
        pass

    @abstractmethod
    def consultar(self):
        pass

    @abstractmethod
    def buscar(self, id: int):
        pass

    @abstractmethod
    def actualizar(self, id: int):
        pass

    @abstractmethod
    def eliminar(self):
        pass
