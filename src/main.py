import random
from juego import Juego
from manada import Manada

# Inicio del main
print("Seleccione el numero de casillas del juego, si quiere el tamaño por defecto pulse ENTER")
numCasillas = input()  # Selecciono el numero de casillas para crear una matriz numCasillas x numCasillas
try:
    if int(numCasillas) > 0 and int(numCasillas) >= 5:
        print("Número de casillas del juego :", numCasillas)
        # Si escribo un numero entero lo acepto
    else:
            print("Escriba un numero entero positivo o si quiere coger el tamaño por defecto escriba cualquer letra: ")
            numCasillas = input()
            if int(numCasillas) > 0:
                if int(numCasillas) < 5:
                    print("No se puede crear un tablero con tan pocas piezas, por lo que se pondrá el tamaño por defecto 75x75")
                    numCasillas = 75
                else:
                    print("Número de casillas del juego :", numCasillas)
            elif int(numCasillas) < 0:
                numCasillas = 75
except:
    #  Si no es un numero valido elijo el valor por defecto 75
    numCasillas = 75
    print("Número de casillas del juego :", 75)

maximoCasillas = int(numCasillas) * int(numCasillas)
numCebras = 0
numLeones = 0
numHienas = 0
# Hago las comprobaciones necesarias para que el numero de cebras sea valido en funcion del numero de casillas seleccionado
while numCebras <= 0 or numCebras >= maximoCasillas or numLeones + numHienas + numCebras >= maximoCasillas:
    numLeones = random.randint(2, int(numCasillas))
    numCebras = numLeones * 6
    numHienas = numLeones * 3
print("NumLeones ", numLeones, " , numHienas ", numHienas, " y numCebras ", numCebras)
# El random esta de 2 a numAnimal para que como minimo haya dos manadas
numeroManadasCebras = random.randint(2, numCebras)
print("NumManadasCebras",numeroManadasCebras)
numeroManadasLeones = random.randint(2, numLeones)
print("NumManadasLeones",numeroManadasLeones)
numeroManadasHienas = random.randint(2, numHienas)
print("NumManadasHienas",numeroManadasHienas)
# Con estas variables selecciono el numero de animales por manada
cuantasCebras = numCebras // numeroManadasCebras
cuantosLeones = numLeones // numeroManadasLeones
cuantasHienas = numHienas // numeroManadasHienas
manadaCebra = []
manadaLeon = []
manadaHiena = []
# Comienzo el juego
juego = Juego(numCasillas, manadaLeon, manadaHiena, manadaCebra)
# Creo las manadas de los distintos tipos de animales
for j in range(0, numeroManadasCebras):
    manadaCebra.append(Manada("Cebra", cuantasCebras, j, juego))
for j in range(0, numeroManadasLeones):
    manadaLeon.append(Manada("Leon", cuantosLeones, j, juego))
for j in range(0, numeroManadasHienas):
    manadaHiena.append(Manada("Hiena", cuantasHienas, j, juego))
# Obtengo las listas de los animales
listaCebras = juego.getListaManadas("Cebra")
listaHienas = juego.getListaManadas("Hiena")
listaLeones = juego.getListaManadas("Leon")
listaHilos = []

for i in range(0, len(listaCebras)):
    for j in range(0, cuantasCebras):
        cebras = listaCebras[i].getAnimal(j) # Selecciono la cebra de la lista de manadas
        juego.insertarAnimal(cebras) # Inserto ese animal en el juego
        listaHilos.append(cebras) # Añado ese animal a la lista de hilos
juego.comprobardiferenciaManada("Cebra", manadaCebra, numeroManadasCebras, numCebras)
# Compruebo que el numero de cebras en las manadas coincida con el numero de cebras establecido al principio
for i in range(0, len(listaHienas)):
    for j in range(0, cuantasHienas):
        hienas = listaHienas[i].getAnimal(j)  # Selecciono la hiena de la lista de manadas
        juego.insertarAnimal(hienas)  # Inserto ese animal en el juego
        listaHilos.append(hienas)  # Añado ese animal a la lista de hilos
juego.comprobardiferenciaManada("Hiena", manadaHiena, numeroManadasHienas, numHienas)
# Compruebo que el numero de hienas en las manadas coincida con el numero de hienas establecido al principio
for i in range(0, len(listaLeones)):
    for j in range(0, cuantosLeones):
        leones = listaLeones[i].getAnimal(j)  # Selecciono el leon de la lista de manadas
        juego.insertarAnimal(leones)  # Inserto ese animal en el juego
        listaHilos.append(leones)  # Añado ese animal a la lista de hilos
juego.comprobardiferenciaManada("Leon", manadaLeon, numeroManadasLeones, numLeones)
# Compruebo que el numero de leones en las manadas coincida con el numero de leones establecido al principio
print()
juego.mostrarTablero()  # Muestro la posicion inicial del tablero con toods los animales insertados
print()
for i in listaHilos:
    i.start()  # Llamo en cada hilo a su metodo start que a su vez llamara al run de cada animal
for i in listaHilos:
    i.join()  # Con join esperamos a que termine la ejecucion de los hilos
print()
juego.mostrarTablero()  # muestro la posicion final del tablero del juego
print()
print("Ganador del juego la manada", juego.getManadaGanadora()[0], "de", juego.getManadaGanadora()[2], "con una puntuacion de", juego.getManadaGanadora()[1])
# La posicion 0 representa el numero de la manada
# la posicion 1 representa los puntos obtenidos por la manada
# la posicon 2 representa la especie de la manada ganadora
