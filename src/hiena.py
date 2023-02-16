import random
import threading
import time

from animal import Animal
from cebra import Cebra


class Hiena(Animal, threading.Thread):

    def __init__(self, numManada, juego):
        super().__init__("Hiena", numManada)  # Inicializo la especie a Hiena y le paso el numManada
        self.__juego = juego  # Añado el atributo juego para tener acceso a la variable ganador
        threading.Thread.__init__(self)  # Inicializo el Thread para poder sobrescribir el metodo run

    def run(self):
        while not self.__juego.getGanador():  # Mientras que no haya ganador en el juego
            if self.getEstado():  # Si la hiena esta viva
                time.sleep(self.getVelocidad())  # Esperamos en funcion de la velocidad de la manada de la hiena
                if not self.__juego.getGanador():  # Vuelvo a comprobar por si han modificado la variable ganador en este tiempo
                    queHacer = random.randint(0, 2)
                    if queHacer == 0:  # Si el numero aleatorio es 0 entonces el animal caza
                        self.cazar()
                    elif queHacer == 1:  # Si el numero aleatorio es 1 entonces el animal se mueve
                        self.moverse(self.__juego)
                    elif queHacer == 2:  # Si el numero aleatorio es 2 entonces el animal no hace nada
                        pass
                    if self.puedeDescansar():
                        self.descansar()
            else:
                return

    def puedeCazar(self, fila, columna):
        posiciones = self.__juego.getPosicionesAdyacentesAnimal(self)[0]
        tablero = self.__juego.getTablero()
        contCebras = 0
        contHienas = 1
        # La comprobacion para cazar de las hienas es parecido al de los leones
        # Tenemos que contar en las casillas adyacentes el numero de cebras y de hienas
        if tablero[fila][columna].getAnimal().getEspecie == "Cebra":
            for i in range(0, len(posiciones)):
                if str(tablero[posiciones[i][0]][posiciones[i][1]]) == "Hiena":
                    contHienas = contHienas + 1
                elif str(tablero[posiciones[i][0]][posiciones[i][1]]) == "Cebra":
                    contHienas = contCebras + 1
        # Si el numero de hienas es mayor al de cebras entonces podra cazarla sino no podra
        if contHienas > contCebras:
            return True
        else:
            return False

    def cazar(self):
        posicionesOcupadas = self.__juego.getPosicionesAdyacentesAnimal(self)[1]
        # Obtengo las posiciones adyacentes ocupadas
        if len(posicionesOcupadas) == 0:
            self.__juego.bloquearMutexES()
            print(self.__str__+" no puede cazar porque no tiene animales alrededor")
            self.__juego.liberarMutexES()
        else:
            # Si las posiciones no son vacias
            tablero = self.__juego.getTablero()
            posicionRandom = random.randint(0, len(posicionesOcupadas) - 1)
            casilla = posicionesOcupadas[posicionRandom]
            puedeCazar = self.puedeCazar(casilla[0], casilla[1])
            # Elijo una posicion al azar y compruebo si puede cazar
            if puedeCazar:
                # Si puede cazar hago el mismo procedimiento que con los leones para cazar cebras
                if tablero[casilla[0]][casilla[1]].getAnimal().getEspecie == "Cebra":
                    tablero[casilla[0]][casilla[1]].bloquearMutex()
                    numManada = tablero[casilla[0]][casilla[1]].getAnimal().getNumManada
                    tablero[casilla[0]][casilla[1]].getAnimal().setEstadoMuerto()
                    tablero[casilla[0]][casilla[1]].setCasillaFalse()
                    tablero[self.getFila()][self.getColumna()].bloquearMutex()
                    tablero[self.getFila()][self.getColumna()].setCasillaFalse()
                    tablero[casilla[0]][casilla[1]].setAnimal(self)
                    tablero[casilla[0]][casilla[1]].setCasillaTrue()
                    tablero[self.getFila()][self.getColumna()].liberarMutex()
                    tablero[casilla[0]][casilla[1]].liberarMutex()
                    self.setFila(casilla[0])
                    self.setColumna(casilla[1])
                    self.__juego.bloquearMutexES()
                    print(self.__str__ + " Ha cazado una Cebra de la manada "+str(numManada) +" en " + str(self.getFila()) + " " + str(self.getColumna()))
                    self.__juego.liberarMutexES()
                    nuevaCebra = Cebra(numManada, self.__juego)
                    self.__juego.insertarAnimal(nuevaCebra)
                    self.__juego.bloquearMutexES()
                    print("Nueva Cebra de la manada " + str(numManada) + " creada en posicion " + str(nuevaCebra.getFila()) + " " + str(nuevaCebra.getColumna()))
                    self.__juego.liberarMutexES()
                    self.__juego.sumarPuntos(self.getEspecie, self.getNumManada, 1)
                    nuevaCebra.start()




