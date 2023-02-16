import threading
from animal import Animal

class Casilla:

    def __init__(self, especie=""):
        self.__animal = Animal(especie)
        self.__mutex = threading.Lock()
        self.__habitado = False
        # La casilla consta de un animal, un mutex para poder bloquear la casilla y un booleando habitado que dice si hay algún animal o no

    # Getters y setters para acceder a los atributos privados
    def getEstadoMutex(self):
        return self.__mutex.locked()

    def bloquearMutex(self):
        self.__mutex.acquire()

    def liberarMutex(self):
        self.__mutex.release()

    def getCasilla(self):
        return self

    def getHabitado(self):
        return self.__habitado

    def getAnimal(self):
        return self.__animal

    def setAnimal(self, animal : Animal):
        self.__animal = animal

    def setCasillaTrue(self):
        self.__habitado = True

    def setCasillaFalse(self):
        self.__habitado = False

    # Este metodo permite mostrar el tablero de juego si el animal esta vivo y tiene especie muestra su toString sino muestra "-"
    def __str__(self) -> str:
        if self.__animal.getEspecie != "":
            if self.__habitado:
                return self.__animal.__str__
            else:
                return "-"
        else:
            return "-"
