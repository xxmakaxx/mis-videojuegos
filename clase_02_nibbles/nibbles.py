import random
import sys
import pygame

pygame.init()

ANCHO, ALTO = 600, 600  # Define el tamaño de la ventana
CELDA = 30  # Cada cuadrado del tablero medirá 30x30 píxeles
COLUMNAS = ANCHO // CELDA  # Calcula cuántas columnas tendrá el tablero. Tendrá 20 columnas
FILAS = ALTO // CELDA  # Calcula cuántas filas tendrá el tablero. Tendrá 20 filas

pantalla = pygame.display.set_mode((ANCHO, ALTO))  # Crea la ventana del juego
reloj = pygame.time.Clock()  # Crea un reloj para controlar la velocidad del juego

# El cuerpo: lista de (columna, fila). La cabeza es el primer elemento
# Dentro de la lista hay una tupla. La serpiente empieza en la columna 5, fila 5
serpiente = [(5, 5)]

direccion = (1, 0)
# (dx, dy) -> derecha.
# Define la dirección inicial.
# Avanzará una columna y no se moverá verticalmente.


def manzana_nueva():  # Crea una manzana en una posición aleatoria
    while True:
        m = (
            random.randint(0, COLUMNAS - 1),
            random.randint(0, FILAS - 1)
        )  # Genera una posición aleatoria

        if m not in serpiente:
            # Comprueba que la manzana no aparezca encima de la serpiente
            return m  # Devuelve la posición encontrada


manzana = manzana_nueva()  # Crea la primera manzana
puntos = 0  # El marcador empieza en 0

try:
    with open("record.txt") as f:
        record = int(f.read())
except FileNotFoundError:
    record = 0  # Si no existe el archivo, el récord es 0


manzana_dorada = None  # No hay manzana dorada al inicio


def dibujar_celdas(pos, color):
    # Define la función que recibe datos de posición y color

    pygame.draw.rect(
        pantalla,
        color,
        (
            pos[0] * CELDA,
            pos[1] * CELDA,
            CELDA - 2,
            CELDA - 2
        )
    )

    # pos[0]: obtiene la columna
    # pos[1]: obtiene la fila
    # pos[0] * CELDA: convierte la columna en píxeles
    # CELDA - 2: el cuadrado será dos píxeles más pequeño


ejecutando = True

while ejecutando:  # Comienza el bucle principal del juego

    # LEER ENTRADA
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            # Comprueba si el jugador cerró la ventana
            ejecutando = False

        elif evento.type == pygame.KEYDOWN:
            # Comprueba si pulsó una tecla

            # No dejar que gire 180 grados (no puede ir atrás)

            if evento.key == pygame.K_UP and direccion != (0, 1):
                # Si se pulsa la flecha hacia arriba y la serpiente
                # no está bajando, cambiará de dirección
                direccion = (0, -1)

            elif evento.key == pygame.K_DOWN and direccion != (0, -1):
                # Si se pulsa la flecha hacia abajo y la serpiente
                # no está subiendo, cambiará de dirección
                direccion = (0, 1)

            elif evento.key == pygame.K_LEFT and direccion != (1, 0):
                # Si se pulsa la flecha izquierda y la serpiente
                # no está avanzando hacia la derecha, girará hacia la izquierda
                direccion = (-1, 0)

            elif evento.key == pygame.K_RIGHT and direccion != (-1, 0):
                # Si se pulsa la flecha derecha y la serpiente
                # no está avanzando hacia la izquierda, girará hacia la derecha
                direccion = (1, 0)


    # 1) Nueva cabeza
    cabeza = (
        serpiente[0][0] + direccion[0],
        serpiente[0][1] + direccion[1]
    )

    # Si la cabeza está en (5, 5) y la dirección es (1, 0),
    # la nueva posición será (6, 5)

    serpiente.insert(0, cabeza)
    # Inserta la nueva cabeza en la primera posición de la lista


    # 2) ¿Comió?
    comio = False

    if cabeza == manzana:
        # Comprueba si la serpiente ha comido la manzana
        puntos += 1
        # Suma un punto
        manzana = manzana_nueva()
        # Crea una nueva manzana

        if random.randint(1, 10) == 1:
            manzana_dorada = manzana_nueva()
        else:
            manzana_dorada = None

        comio = True

    elif cabeza == manzana_dorada:
        puntos += 5
        # Suma cinco puntos
        manzana_dorada = None
        # La manzana dorada desaparece
        comio = True

    if puntos > record:
        record = puntos
        with open("record.txt", "w") as f:
             f.write(str(record))

    if not comio:
        serpiente.pop()
        # Elimina el último segmento de la serpiente.
        # Esto da la sensación de movimiento.


    # 3) ¿Chocó con el borde o consigo misma?
    if (
        cabeza[0] < 0
        or cabeza[0] >= COLUMNAS
        or cabeza[1] < 0
        or cabeza[1] >= FILAS
        or cabeza in serpiente[1:]
    ):
        # Comprueba si la serpiente ha chocado.
        # Puede ocurrir en dos situaciones:
        # 1. Choca contra una pared.
        # 2. Choca contra su propio cuerpo.

        ejecutando = False
        # El juego termina


    # 4) Dibujar
    pantalla.fill((10, 10, 15))
    # Pinta el fondo de un color oscuro

    for segmento in serpiente:
        # Recorre todos los segmentos de la serpiente

        dibujar_celdas(segmento, (0, 220, 60))
        # Dibuja cada segmento de color verde

    dibujar_celdas(manzana, (230, 40, 40))
    # Dibuja la manzana de color rojo

    if manzana_dorada is not None:
        dibujar_celdas(manzana_dorada, (255, 215, 0))
    # Dibuja la manzana dorada de color dorado

    pygame.display.set_caption(f"Puntos: {puntos} | Récord: {record}")
    # Actualiza el título de la ventana

    pygame.display.flip()
    # Actualiza la pantalla

    reloj.tick(10)
    # 5 FPS: la serpiente avanza 5 veces por segundo


# Estas líneas están FUERA del while,
# por eso solo se ejecutan cuando termina el juego.

pygame.quit()
print(f"Fin del juego. Puntos: {puntos}")
sys.exit()

#Por que la serpiente se mueve sin apretar nada? 
#direccion(1, 0) significa que la direccion inicial de la serpiente es hacia la derecha
#Dentro del while, donde se define cabeza = (...) esto calcula continuamente donde estara la siguiente cabeza
#Luego en serpiente.insert(..) agrega esa nueva posicion como cabeza
#Finalmente serpiente.pop() elimina la cola anterior, entonces ocurre esto: (5,5) -> (6,5) -> (7,5) -> (8,5) -> (9,5) -> (10,5) y asi sucesivamente.
#Y como reloj.tick(10) el juego repite ese proceso 10 veces por segundo.
#Las teclas solo cambian la direccion de la serpiente..

#Que pasa si cambias el reloj.tick(10) por tick(20)?
#La serpiente de movera el doble de rapido, avanzara 20 veces por segundo. Esto hace que el juego sea mas dificil.

#Por que cabeza in serpiente[1:] detecta la mordida a si misma?
#Porque serpiente[1:] devuelve todos los segmentos de la serpiente excepto la cabeza. Entonces si la cabeza esta en la misma posicion que algun segmento del cuerpo, significa que se mordio a si misma.