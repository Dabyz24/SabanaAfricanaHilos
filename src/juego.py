import random
from threading import Lock
from typing import List
from casilla import Casilla
from manada import Manada
from animal import Animal


class Juego:
    def __init__(self, numCasillas, manadaLeones: List[Manada], manadaHienas: List[Manada], manadaCebras: List[Manada]):
        self.__numCasillas = int(numCasillas)  # Es necesario convertirlo porque en el main lo obtengo como un string
        self.__tablero = [] * self.__numCasillas
        for i in range(self.__numCasillas):
            self.__tablero.append([])
            for j in range(self.__numCasillas):
                self.__tablero[i].append(Casilla())
        # Creo la matriz de casillas para poder empezar el juego el tamaños sera numCasillas x numCasillas
        self.__manadaLeones = manadaLeones
        self.__manadaHienas = manadaHienas
        self.__manadaCebras = manadaCebras
        # Guardo cada una de las manadas en el juego
        self.__ganador = False
        self.__mutexGanador = Lock()
        self.__manadaGanadora = [0, 0, ""]
        self.__mutexEntradaSalida = Lock()
        # El booleano ganador decidira si se acaba el juego o no por lo que necesitara un mutex para que no puedan acceder dos animales a la vez

    def getTablero(self):
        return self.__tablero

    def getGanador(self):
        return self.__ganador

    def mostrarTablero(self):
        a = ""
        for k in range(self.__numCasillas):
            for j in range(self.__numCasillas):
                a += str(self.__tablero[k][j]) + '\t'
            print(a)
            a = ""
    # Este método permite insertar un animal en la matriz
    def insertarAnimal(self, animal: Animal):
        animal.setFila(random.randint(0, self.__numCasillas - 1))
        animal.setColumna(random.randint(0, self.__numCasillas - 1))
        self.__tablero[animal.getFila()][animal.getColumna()].bloquearMutex()
        # Selecciono un numero aleatorio de la matriz de casillas, mientras que la casilla no este vacia genero otro numero aleatorio
        while str(self.__tablero[animal.getFila()][animal.getColumna()]) != "-":
            if self.__tablero[animal.getFila()][animal.getColumna()].getEstadoMutex():
                self.__tablero[animal.getFila()][animal.getColumna()].liberarMutex()
            animal.setFila(random.randint(0, self.__numCasillas - 1))
            animal.setColumna(random.randint(0, self.__numCasillas - 1))
            self.__tablero[animal.getFila()][animal.getColumna()].bloquearMutex()
        # Con esto evito que una misma casilla tenga varios animales
        self.__tablero[animal.getFila()][animal.getColumna()].setAnimal(animal)  # Establezco el animal en la casilla
        self.__tablero[animal.getFila()][animal.getColumna()].setCasillaTrue()  # Establezco el booleando habitado a True
        # Antes de escribir por ES utilizo el mutex del animal para bloquear la E y S con el objetivo de que los mensajes salgan ordenados
        self.bloquearMutexES()
        print(animal.getEspecie +" "+str(animal.getNumManada)+" insertado en posicion inical "+str(animal.getFila())+" "+str(animal.getColumna()))
        self.liberarMutexES()
        self.__tablero[animal.getFila()][animal.getColumna()].liberarMutex()
        # Para terminar libero el mutex de la casilla
        return self.__tablero

    # Gracias a este método puedo conocer las posiciones adyacentes a unas que les pase por parametro
    def getPosicionesAdyacentes(self, fila, columna):
        indices = []
        if fila > 0:
            if fila + 1 == self.__numCasillas and columna + 1 == self.__numCasillas:
                if columna > 0:
                    indices.append((fila - 1, columna - 1))
                    indices.append((fila - 1, columna))
                else:
                    indices.append((fila - 1, columna))
            elif fila + 1 == self.__numCasillas and columna == 0:
                indices.append((fila - 1, columna))
                indices.append((fila - 1, columna + 1))

            elif fila + 1 > self.__numCasillas:
                return []
            elif columna > 0 and columna + 1 == self.__numCasillas:
                indices.append((fila - 1, columna - 1))
                indices.append((fila - 1, columna))
            elif columna > 0:
                indices.append((fila - 1, columna - 1))
                indices.append((fila - 1, columna))
                indices.append((fila - 1, columna + 1))
            else:
                indices.append((fila - 1, columna))
                indices.append((fila - 1, columna + 1))
        if columna > 0:
            if columna + 1 == self.__numCasillas or fila + 1 == self.__numCasillas:
                indices.append((fila, columna - 1))
            elif columna + 1 > self.__numCasillas:
                return []
            else:
                indices.append((fila, columna - 1))
                indices.append((fila + 1, columna - 1))
        if columna + 1 < self.__numCasillas:
            indices.append((fila, columna + 1))
        if fila + 1 < self.__numCasillas:
            indices.append((fila + 1, columna))
            if columna + 1 < self.__numCasillas:
                indices.append((fila + 1, columna + 1))
            else:
                indices.append((fila + 1, columna - 1))
        # La lista indices contiene una tupla donde la primera posicion [0] es la fila y la segunda posicion [1] es la columna
        return indices

    def getPosicionesAdyacentesAnimal(self, animal):
        indicesAdya = self.getPosicionesAdyacentes(animal.getFila(), animal.getColumna())
        # Obtengo la lista de adyacentes a la posicion del animal
        resultado = []
        resultadoOcupado = []
        resultadoLibre = []
        for i in range(0, len(indicesAdya)):
            # Recorriendo la lista de adyacentes bloqueo el mutex y compruebo si esta ocupada o libre
            self.__tablero[indicesAdya[i][0]][indicesAdya[i][1]].bloquearMutex()
            if self.__tablero[indicesAdya[i][0]][indicesAdya[i][1]].getHabitado():
                resultadoOcupado.append((indicesAdya[i][0], indicesAdya[i][1]))
                resultado.append((indicesAdya[i][0], indicesAdya[i][1]))
            else:
                resultado.append((indicesAdya[i][0], indicesAdya[i][1]))
                resultadoLibre.append((indicesAdya[i][0], indicesAdya[i][1]))
            if self.__tablero[indicesAdya[i][0]][indicesAdya[i][1]].getEstadoMutex():
                self.__tablero[indicesAdya[i][0]][indicesAdya[i][1]].liberarMutex()
            # Al final libero el mutex de la casilla para que no se quede permanentemente bloqueado
            # resultado es la lista con todas las posiciones adyacentes
            # resultadoOcupado es la lista con todas las posiciones adyacentes ocupadas
            # resultadoLibre es la lista con todas las posiciones adyacentes libres
        return resultado, resultadoOcupado, resultadoLibre

    # Para obtener la lista de manadas dependiendo de la especie del animal
    def getListaManadas(self, especie):
        if especie == "Leon":
            return self.__manadaLeones
        elif especie == "Hiena":
            return self.__manadaHienas
        elif especie == "Cebra":
            return self.__manadaCebras

    def getManadaGanadora(self):
        return self.__manadaGanadora
    # Método que permite modificar la puntuacion de cada manada y dar el ganador del juego
    def sumarPuntos(self, especie, numeroManada, i):
        if especie == "Leon":
            self.__manadaLeones[numeroManada].setPuntuacion(i)  # Añado la puntuacion a la puntuacion de la manada
            if self.__manadaLeones[numeroManada].getPuntuacion() >= 20:
                self.bloquearMutexganador()
                # Bloqueo el mutex de la variable ganador y modifico su valor
                self.__ganador = True
                self.liberarMutexganador()
                # Si hay un ganador igualo la manadaGanadora a la manada del leon
                self.__manadaGanadora = [numeroManada, self.__manadaLeones[numeroManada].getPuntuacion(), "Leones"]
            return self.__manadaLeones[numeroManada].getPuntuacion()
        elif especie == "Hiena":
            self.__manadaHienas[numeroManada].setPuntuacion(i)
            if self.__manadaHienas[numeroManada].getPuntuacion() >= 20:
                self.bloquearMutexganador()
                self.__ganador = True
                self.liberarMutexganador()
                self.__manadaGanadora = [numeroManada, self.__manadaHienas[numeroManada].getPuntuacion(), "Hienas"]
                return

    # Este metodo me permite añadir los animales que no se han generado al principio
    def comprobardiferenciaManada(self, tipoAnimal ,manada, numManada, numAnimal):
        if len(manada) < numAnimal and numManada < numAnimal:
            cuantosAnimales = numAnimal // numManada  # Representa el numero de animales por manada
            if cuantosAnimales == 1:
                diferencia = numAnimal - numManada
            elif cuantosAnimales * numManada < numAnimal:
                diferencia = numAnimal - (cuantosAnimales * numManada)
            else:
                diferencia = len(manada) - numManada
            if diferencia != 0:
                print("Añadimos", diferencia, "del tipo de animal:", tipoAnimal)
            # añadira tantos animales como sea diferencia
            for i in range(0, diferencia):
                listaAnimal = self.getListaManadas(tipoAnimal)
                listaAnimal[i].insertatAnimalenManada(tipoAnimal, i)
                animal = listaAnimal[i].getAnimal(0)
                self.insertarAnimal(animal)
        return self

    def bloquearMutexganador(self):
        self.__mutexGanador.acquire()

    def liberarMutexganador(self):
        self.__mutexGanador.release()

    def bloquearMutexES(self):
        self.__mutexEntradaSalida.acquire()

    def liberarMutexES(self):
        self.__mutexEntradaSalida.release()