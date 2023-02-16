import random
import threading
import time
from animal import Animal


class Cebra(Animal, threading.Thread):
    def __init__(self, numManada, juego):
        super().__init__("Cebra", numManada)  # Inicializo la especie a Cebra y le paso el numManada
        self.__juego = juego  # Añado el atributo juego para tener acceso a la variable ganador
        threading.Thread.__init__(self)  # Inicializo el Thread para poder sobreescribir el metodo run

    def run(self):
        while not self.__juego.getGanador():
            if self.getEstado():  # Si el animal se encuentra vivo puede hacer sus funciones
                if not self.__juego.getGanador():  #  Comprobacion para que no sigan ejecutando si han entrado al bucle y modifican el valor de ganador
                    time.sleep(self.getVelocidad())  # Esperamos en funcion de la velocidad de la manada de la cebra
                    queHacer = random.randint(0, 1)
                    if queHacer == 0:
                        self.moverse(self.__juego)  # Se mueve el animal a sus casillas adyacentes
                    elif queHacer == 1:  # Si el numero es 1 no hace nada
                        pass
                    if self.puedeDescansar():
                        self.descansar()
            else:
                #  Si el animal ha sido cazado no hara ninugna funcion y el hilo se quedara en estado zombie
                return


