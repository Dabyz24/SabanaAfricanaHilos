import threading

from leon import Leon
from hiena import Hiena
from cebra import Cebra


class Manada:
    def __init__(self, especie, numeroIntegrantes, numManada, juego):
        self.__manada = []  # Representa la lista de animales que habra en la manada
        self.__puntuacion = 0  # Puntuacion global para los animales pertenecientes a la manada
        self.__mutexPuntuacion = threading.Lock()
        self.__juego = juego  # Necesario para poder crear los animales en las distintas manadas
        if especie == "Leon":
            for i in range(0, numeroIntegrantes):
                le = Leon(numManada, juego)
                le.setVelocidad(numManada/10000+0.000001)
                # El leon es el animal mas rapido y le sumo 0.000001 para que la manada 0 tenga una velocidad distinta a 0
                self.__manada.append(le)
        elif especie == "Cebra":
            for i in range(0, numeroIntegrantes):
                ce = Cebra(numManada, juego)
                ce.setVelocidad(numManada/9000+0.000005)
                # La cebra es el segundo animal mas rapido de la simulacion y si la manada es 0 tendra 0.000005
                self.__manada.append(ce)

        elif especie == "Hiena":
            for i in range(0, numeroIntegrantes):
                hi = Hiena(numManada, juego)
                hi.setVelocidad(numManada/8000 + 0.000009)
                # La Hiena es el tercer animal mas rapido de la simulacion
                self.__manada.append(hi)

    # Para añadir algún animal nuevo a la manada con numManada
    def insertatAnimalenManada(self, animal, numManada):
        if animal == "Cebra":
            return self.__manada.append(Cebra(numManada, self.__juego))
        elif animal == "Hiena":
            return self.__manada.append(Hiena(numManada, self.__juego))
        elif animal == "Leon":
            return self.__manada.append(Leon(numManada, self.__juego))

    # Getters y setters necesarios para manipular los atributos privados de la manada
    def getPuntuacion(self):
        return self.__puntuacion

    def getAnimal(self, pos):
        return self.__manada[pos]

    def setPuntuacion(self, puntos):
        self.__mutexPuntuacion.acquire()
        self.__puntuacion = self.__puntuacion + puntos
        self.__mutexPuntuacion.release()
        return self.__puntuacion

    @property
    def getListaManada(self):
        return self.__manada

    def __str__(self):
        for i in range(0, len(self.__manada)):
            return self.__manada[i].__str__
