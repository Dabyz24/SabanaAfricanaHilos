import random
import time


class Animal:

    def __init__(self, especie: str, numManada=0):
        # Declaro todos los atributos como privados para que solo se puedan acceder mediante metodos por otras clases
        self.__especie = especie
        self.__numManada = numManada
        self.__casillaFila = 0
        self.__casillaColumna = 0
        self.__estado = True
        self.__velocidad = 0

    def moverse(self, juego):
        # Obtengo las posiciones adyacentes libres
        tablero = juego.getTablero()
        listaAdyacentes = juego.getPosicionesAdyacentesAnimal(self)[2]
        posicionInicialFil = self.__casillaFila
        posicionInicialCol = self.__casillaColumna
        # Si no hay ninguna posicion libre el animal se queda en la misma posicion y no hace nada mas
        if len(listaAdyacentes) == 0:
            juego.bloquearMutexES()
            print(self.__str__ + " se queda en la misma posicion con fila " + str(self.__casillaFila) + " y columna " + str(self.__casillaColumna))
            juego.liberarMutexES()
            return
        else:
            # Si hay alguna posicion libre
            posicion = random.randint(0, len(listaAdyacentes) - 1)
            posicionNueva = listaAdyacentes[posicion]
            # Elijo la posicion libre al azar y bloqueo el mutex de la posicion inicial
            tablero[posicionInicialFil][posicionInicialCol].bloquearMutex()
            # Establezco la casilla como desocupada
            tablero[posicionInicialFil][posicionInicialCol].setCasillaFalse()
            # Establezco la fila y la columna del animal en la nueva posicion
            self.__casillaFila = posicionNueva[0]
            self.__casillaColumna = posicionNueva[1]
            # Bloqueo el mutex de la nueva posicion y pongo el animal en la casilla nueva
            tablero[self.__casillaFila][self.__casillaColumna].bloquearMutex()
            tablero[self.__casillaFila][self.__casillaColumna].setAnimal(self)
            tablero[self.__casillaFila][self.__casillaColumna].setCasillaTrue()
            # Por ultimo libero los mutex de las casillas iniciales y destino
            tablero[self.__casillaFila][self.__casillaColumna].liberarMutex()
            tablero[posicionInicialFil][posicionInicialCol].liberarMutex()
            juego.bloquearMutexES()
            print(self.__str__ + " se ha movido a la nueva fila " + str(self.__casillaFila) + " y columna " + str(self.__casillaColumna))
            juego.liberarMutexES()
        return

    def puedeDescansar(self):
        # Para los animales excepto los leones la proporcion para descansar sera de 1/3
        if random.randint(0, 2) < 1:
            return True
        else:
            return False

    def descansar(self):
        # El metodo descansar sera un sleep entre 0 y 1 pudiendo ser el resultado del random con decimales
        time.sleep(random.uniform(0, 1))
        return
    # Declaro los getters y setters necesarios para obtener los atributos privados de la clase
    @property
    def getEspecie(self):
        return self.__especie

    def setEspecieVacio(self):
        self.__especie = ""

    @property
    def getNumManada(self):
        return self.__numManada

    def getFila(self):
        return self.__casillaFila

    def setFila(self, fila):
        self.__casillaFila = fila

    def getColumna(self):
        return self.__casillaColumna

    def setColumna(self, columna):
        self.__casillaColumna = columna

    def getEstado(self):
        return self.__estado

    def setEstadoMuerto(self):
        self.__estado = False

    def getVelocidad(self):
        return self.__velocidad

    def setVelocidad(self, velocidad):
        self.__velocidad = velocidad

    # Declaro el toString de la clase animal para que se sepa con claridad cual es el animal correspondiente
    @property
    def __str__(self):
        return self.__especie +" "+str(self.__numManada)
