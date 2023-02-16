import random
import threading
import time

from animal import Animal
from cebra import Cebra


class Leon(Animal, threading.Thread):
    def __init__(self, numManada, juego):
        super().__init__("Leon", numManada)  # Inicializo la especie a Leon y le paso el numManada
        self.__juego = juego  # Añado el atributo juego para tener acceso a la variable ganador
        threading.Thread.__init__(self)  # Inicializo el Thread para poder sobreescribir el metodo run

    def run(self):
        while not self.__juego.getGanador():
            time.sleep(self.getVelocidad())  # Esperamos en funcion de la velocidad de la manada del leon
            if not self.__juego.getGanador():
                queHacer = random.randint(0, 2)
                if queHacer == 0:  # Si el numero aleatorio es 0 puede cazar
                    self.cazar()
                elif queHacer == 1:  # Si el numero aleatorio es 1 decidira moverse
                    self.moverse(self.__juego)
                elif queHacer == 2:  # Si el numero aleatorio es 2 no hace nada
                    pass
                if self.puedeDescansar():
                    self.descansar()

    def puedeCazar(self, fila, columna):
        posiciones = self.__juego.getPosicionesAdyacentesAnimal(self)[0]  # Obtengo todas las posiciones adyacentes al animal
        tablero = self.__juego.getTablero()
        contLeones = 1
        contHienas = 0
        if tablero[fila][columna].getAnimal().getEspecie == "Cebra":
            # Si en la casilla especificada para cazar se encuentra una cebra siempre podra cazarla
            return True
        elif tablero[fila][columna].getAnimal().getEspecie == "Hiena":
            # Si se encuentra una hiena tendra que recorrer todas las casillas adyacentes para contar el numero de hienas y leones
            for i in range(0, len(posiciones)):
                if str(tablero[posiciones[i][0]][posiciones[i][1]]) == "Hiena":
                    contHienas = contHienas + 1
                elif str(tablero[posiciones[i][0]][posiciones[i][1]]) == "Leon":
                    contLeones = contLeones + 1
            if contLeones >= contHienas:
                # Si el numero de leones es igual o superior al de hienas adyacentes podra cazarlo
                return True
            else:
                # Si no es mayor o igual no podra cazarlo
                return False

    def cazar(self):
        posicionesOcupadas = self.__juego.getPosicionesAdyacentesAnimal(self)[1]
        # Selecciono las posiciones ocupadas adyacentes al animal
        if len(posicionesOcupadas) == 0:
            self.__juego.bloquearMutexES()
            print(self.__str__+" no puede Cazar porque no tiene animales alrededor")
            self.__juego.liberarMutexES()
        else:
            # Si tiene 1 o mas posiciones adyacentes ocupadas
            tablero = self.__juego.getTablero()
            posicionRandom = random.randint(0, len(posicionesOcupadas)-1)
            casilla = posicionesOcupadas[posicionRandom]
            # Selecciono una posicion aleatoria de esas posiciones ocupadas
            puedeCazar = self.puedeCazar(casilla[0], casilla[1]) # Compruebo si puede cazar al animal de esa posicion
            if puedeCazar:
                if tablero[casilla[0]][casilla[1]].getAnimal().getEspecie == "Cebra":
                    tablero[casilla[0]][casilla[1]].bloquearMutex()  # Bloqueo la casilla de la presa
                    numManada = tablero[casilla[0]][casilla[1]].getAnimal().getNumManada  # Guardo el numero de la manada de la cebra para despues crearla
                    tablero[casilla[0]][casilla[1]].getAnimal().setEstadoMuerto()  # Pongo el estado de la presa a muerto para que no pueda seguir moviendose
                    tablero[casilla[0]][casilla[1]].setCasillaFalse()  # Establezco la casilla de la cebra como desocupada
                    tablero[self.getFila()][self.getColumna()].bloquearMutex()  # Bloqueo la casilla donde se encuentra el leon
                    tablero[self.getFila()][self.getColumna()].setCasillaFalse()  # Pongo la casilla del leon como desocupada
                    tablero[casilla[0]][casilla[1]].setAnimal(self)  # Establezco el leon en la casilla donde antes estaba la cebra
                    tablero[casilla[0]][casilla[1]].setCasillaTrue()  # Pongo la casilla como ocupada
                    tablero[self.getFila()][self.getColumna()].liberarMutex() # Libero los mutex de las casilla inicial y la casilla final
                    tablero[casilla[0]][casilla[1]].liberarMutex()
                    self.setFila(casilla[0])  # Establezco la fila y la columna del leon en la casilla final
                    self.setColumna(casilla[1])
                    self.__juego.bloquearMutexES()  # Bloqueo el mutex de entrada y salida para escribir el mensaje de caza
                    print(self.__str__+" Ha cazado una Cebra de la manada "+ str(numManada)+" en " + str(self.getFila()) + " " + str(self.getColumna()))
                    self.__juego.liberarMutexES()
                    nuevaCebra = Cebra(numManada, self.__juego)  # Creo una nueva cebra con el mismo numero de manada que la cazada anteriormente
                    self.__juego.insertarAnimal(nuevaCebra)  # Inserto ese animal en el juego
                    self.__juego.bloquearMutexES()
                    print("Nueva Cebra de la manada " + str(numManada) + " creada en posicion " + str(nuevaCebra.getFila()) + " " + str(nuevaCebra.getColumna()))
                    self.__juego.liberarMutexES()
                    self.__juego.sumarPuntos(self.getEspecie, self.getNumManada, 1) # Sumo los puntos a la manada correspondiente por la captura
                    nuevaCebra.start()  # Inicializo la cebra nueva para que pueda jugar libremente en el juego

                elif tablero[casilla[0]][casilla[1]].getAnimal().getEspecie == "Hiena":
                    # En el caso de que se pueda cazar a una hiena el procedimiento es el mismo que con la cebra
                    # Solo que en este caso no crearemos una nueva hiena
                    tablero[casilla[0]][casilla[1]].bloquearMutex()
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
                    print(self.__str__+" ha cazado una Hiena en " + str(self.getFila()) + " " + str(self.getColumna()))
                    self.__juego.liberarMutexES()
                    self.__juego.sumarPuntos(self.getEspecie, self.getNumManada, 2) # Sumamos dos puntos a la manada de leones por la captura de un hiena
            else:
                self.__juego.bloquearMutexES()
                print(self.__str__+" no puede cazar porque no cumple la condicion para cazar")
                self.__juego.liberarMutexES()

    def puedeDescansar(self):
        # El leon es el animal que mayor propension tiene para descansar por lo que tendra 3/4 de probabilidad de descansar
        if random.randint(0, 3) < 0:
            return True
        else:
            return False
