import sys #Importa el modiflo sys, que permite interactuar con el sistema operativo
import pygame #Importa la biblioteca pygame, que permite crear videojuegos

pygame.init() #Inicializa todos los módulos de pygame

ANCHO, ALTO = 800, 600 #El alto de la ventana sera de 800 pixeles y la altura sera de 600 pixeles
pantalla = pygame.display.set_mode((ANCHO, ALTO)) #Crea la ventana con las dimensiones especificadas
#pygame.display controla la pantalla
#set_mode() establece el tamaño de la ventana
#(ANCHO, ALTO) indica sus dimensiones
pygame.display.set_caption("Mi primer juego") #Establece el título de la ventana
reloj = pygame.time.Clock() #Crea un objeto que controla la veloocidad del juego. Más adelante se usará para limitar los FPS (Frames Per Second, cuadros por segundo) del juego

x, y = 100, 100 #Posicion del cuadro
#x es la posicion horizontal
#y es la posicion vertical
velocidad = 5 #La velocidad del cuadro sera de 5 pixeles. Cada vez que se pulse una tecla, el cuadro se movera 5 pixeles

ejecutando = True #Se crea una variable llamada ejecutando, mientras sea True el juego seguirá funcionando
while ejecutando: #Comienza el bucle principal del juego
    #1) LEER ENTRADA
    for evento in pygame.event.get(): #Obtiene todos los eventos que ocurren en el juego. Pulsar tecla, mover el ratón, cerrar la ventana, etc.
        if evento.type == pygame.QUIT: #Comprueba si el usuario ha intentado cerrar la ventana
            ejecutando = False #Si el usuario cierra la ventana, la variable pasa a false y el bucle principal termina, cerrando el juego

    teclas = pygame.key.get_pressed() #Obtiene el estado del teclado. teclas almacena que teclas estan pusladas en ese momento
    x = max(0, min(ANCHO - 50, x)) #Evita que el cuadro se salga de la ventana por la izquierda o derecha
    y = max(0, min(ALTO - 50, y)) #Evita que el cuadro se salga de la ventana por arriba o abajo
    if teclas[pygame.K_LEFT]: #Comprueba si la flecha izquierda del teclado esta pulsada
        x -= velocidad #Resta 5 a x, lo que hace que el cuadro se mueva 5 pixeles a la izquierda
    if teclas[pygame.K_RIGHT]: #Comprueba si la flecha derecha del teclado esta pulsada
        x += velocidad #Suma 5 a x, lo que hace que el cuadro se mueva 5 pixeles a la derecha
    if teclas[pygame.K_UP]: #Comprueba si la flecha arriba del teclado esta pulsada
        y -= velocidad #Resta 5 a y, lo que hace que el cuadro se mueva 5 pixeles hacia arriba
    if teclas[pygame.K_DOWN]: #Comprueba si la flecha abajo del teclado esta pulsada
        y += velocidad #Suma 5 a y, lo que hace que el cuadro se mueva 5 pixeles hacia abajo

    #2) ACTUALIZAR (no hace faltas en este juego tan simple)

    #3) DIBUJAR
    pantalla.fill((20, 20, 40)) #Fondo. fill() rellena la ventana con un color. 20 rojo, 20 verde, 40 de azul. El color es un tono de azul oscuro
    pygame.draw.rect(pantalla, (0, 200, 255), (x, y, 50, 50)) #Dibuja un rectangulo
    #pantalla es en donde se dibuja
    #(0, 200, 255) es el color del rectangulo. Es un tono de azul claro
    #(x, y, 50, 50): x posicion horizontal, y posicion vertical, 50 de ancho y 50 de alto
    pygame.display.flip() #Actualizar pantalla. Sin esto, los cambios realizados no serian visibles

    reloj.tick(60) #Limitar a 60 FPS. Sin esto el cuadrado podria moverse demasiado rapido

pygame.quit() #Cierra todos los módulos de pygame
sys.exit() #Finaliza el programa.