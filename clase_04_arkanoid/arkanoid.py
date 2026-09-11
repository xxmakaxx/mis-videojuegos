import sys
import pygame

pygame.init()

ANCHO, ALTO = 800, 600  # Define el tamaño de la ventana
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()
pala = pygame.Rect(ANCHO // 2 - 60, ALTO - 40, 120, 15)
pelota = pygame.Rect(ANCHO // 2 - 8, ALTO // 2, 16, 16)
vel_x, vel_y = 5, -5

#Ladrillos: cada uno es un dict con su rect, color y puntaje según la fila
FILAS, COLS = 4, 10
COLORES_POR_FILA = [
    (255, 90, 90), #Fila 0 (arriba del todo) - vale más
    (255, 170, 80), #Fila 1
    (255, 230, 90), #Fila 2
    (120, 220, 120), #Fila 3 (abajo del todo) - vale menos
]

PUNTOS_POR_FILA = [40, 30, 20, 10]

#Ladrillos: una fila de rectángulos
ladrillos = []
for fila in range(FILAS):
    for col in range(COLS):
        rect = pygame.Rect(col * 80 + 5, fila * 30 + 40, 70, 20)
        ladrillos.append({
            "rect": rect,
            "color": COLORES_POR_FILA[fila],
            "puntos": PUNTOS_POR_FILA[fila],
        })

vidas = 3
puntaje = 0
ladrillos_destruidos = 0
INCREMENTO_VEL = 0.5 #Cuánto se acelera cada 5 ladrillos

ejecutando = True
gano = False

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    #Paleta sigue al mouse
    pala.x = pygame.mouse.get_pos()[0] - pala.width // 2
    pala.x = max(0, min(ANCHO - pala.width, pala.x))

    #Mover la pelota
    pelota.x += vel_x
    pelota.y += vel_y

    #Rebotes con paredes
    if pelota.left <= 0 or pelota.right >= ANCHO:
        vel_x *= -1
    if pelota.top <= 0:
        vel_y *= -1

    #Rebota en la paleta
    #Se cambia esta parte para obtener el punto (3)
    if pelota.colliderect(pala) and vel_y > 0: 
        #Dónde pegóm relativo al centro de la paleta? Rango: -1 (izq) a 1 (der)
        offset = (pelota.centerx - pala.centerx) / (pala.width / 2)
        offset = max(-1, min(1, offset)) #Por si pega justo en el borde extremo

        MAX_VEL_X = 7 #Que tan abierto puede salir el ángulo
        MIN_VEL_Y = 4 #Para que nunca salga demasiado horizontal

        signo_y = 1 if vel_y > 0 else -1 #Preservamos el signo antes de invertir
        vel_x = offset * MAX_VEL_X
        vel_y = -max(MIN_VEL_Y, 8 - abs(vel_x))

    #Completá: destruir ladrillos
    for ladrillo in ladrillos[:]:
        rect = ladrillo["rect"]
        if pelota.colliderect(rect):
            ladrillos.remove(ladrillo)
            puntaje += 10 * (ladrillo["puntos"] // 10) #10 ptos por ladrillo
            ladrillos_destruidos += 1

            #Cada 5 ladrillos destruidos, acelera la pelota
            if ladrillos_destruidos % 5 == 0:
                vel_x += INCREMENTO_VEL if vel_x > 0 else -INCREMENTO_VEL
                vel_y += INCREMENTO_VEL if vel_y > 0 else -INCREMENTO_VEL

            #Por qué lado la superposición es menor? Ese es el eje del golpe
            solape_x = min(pelota.right, rect.right) - max(pelota.left, rect.left)
            solape_y = min(pelota.bottom, rect.bottom) - max(pelota.top, rect.top)
            if solape_x < solape_y:
                vel_x *= -1 #Golpe lateral
            else:
                vel_y *= -1 #Golpe arriba/abajo
            break

    #Victoria
    if len(ladrillos) == 0:
        gano = True
        ejecutando = False

    #Perder vida
    if pelota.bottom >= ALTO:
        vidas -= 1
        pelota.center = (ANCHO // 2, ALTO // 2)
        if vidas == 0:
            ejecutando = False

    #Dibujar
    pantalla.fill((15, 15, 30))
    pygame.draw.rect(pantalla, (90, 180, 255), pala)
    pygame.draw.rect(pantalla, (255, 255, 255), pelota)
    for ladrillo in ladrillos:
        pygame.draw.rect(pantalla, ladrillo["color"], ladrillo["rect"])

    pygame.display.set_caption(f"Arkanoid - Vidas: {vidas} - Puntaje: {puntaje}  Ladrillos: {len(ladrillos)}")
    pygame.display.flip()
    reloj.tick(60)

#Pantalla final simple
pantalla.fill((15, 15, 30))
fuente = pygame.font.SysFont(None, 64)
if gano:
    texto = fuente.render("Ganaste", True, (120, 255, 120))
else:
    texto = fuente.render("Game Over", True, (255, 100, 100))
rect_texto = texto.get_rect(center=(ANCHO // 2, ALTO // 2))
pantalla.blit(texto, rect_texto)
pygame.display.flip()
pygame.time.wait(2000)

pygame.quit()
sys.exit()

#1) Qué hace exactamente for ladrillo in ladrillos[:] y por qué uso una copia de la lista?
#Cuando se escribe for ladrillo in ladrillos sin [:], Python recorre la lista usando un índice interno que va avanzando: 0, 1, 2, 3... Si se modifica
#la lista mientras la estás recorriendo (por ejemplo, con ladrillos.remove(ladrillo)), esos índices desincronizan de la lista real y podes terminar:
#Saltando elementos sin querer
#En casos más raros, tirando un error o comportándose de forma inconsistente
#Que hace ladrillos[:]? Crea una copia nueva de la lista
#El for recorre la copia, que queda fija y no cambia aunque vos hagas ladrillos.remove(...) sobre la lista original
#Se puede borrar elementos de ladrillos (la original) con total libertad, porque el bucle no está iterando sobre esa misma lista, 
#sino sobbre un duplicado

#2) La pelota de mi Arkanoid atraviesa los ladrillos. Cuál es el problema?
#El problema es que siempre rebota en el mismo eje, sin importar por donde chocó
#La causa raíz:
#for ladrillo in ladrillos[:]:
#    if pelota.colliderect(ladrillo):
#        ladrillos.remove(ladrillo)
#        vel_y *= -1 -> Siempre invierte Y, pase lo que pase
#
#Asume que todos los choques con ladrillos son "por arriba o por abajo" (por eso invierte Y). Pero en realidad,
#la pelota puede chocar con un ladrillo:
#Por arriba/abajo -> invierte Y
#Por izquierda/derecha (entrando de costado a la fila) -> invierte X
#Como se soluciona?
#Hay que decidir que eje invertir según de que lado vino el golpe, no invertir siempre vel_y.
#Una forma simple y muy usada es comparar cuianto se superpone la pelota con el ladrillo en X vs en Y
#El eje con menor superposición es el lado por el que entró

#3) Agregá que la pelota rebote distinto según dónde toque la paleta (izquierda, centro, derecha)
#-Calculamos la distancia entre el centro de la pelota y el centro de la paleta
#-Normalizamos esa distancia a un rango de -1 (bordew izquierdo) a 1 (borde derecho)
#-Usamos ese valor para definir vel_x, y mantenemos una velocidad total constante (o casi) para que el juego no se vuelva
#ni muy lento ni muy rápido.

#offset te dice que tan lejos del centro pegó la pelota, en una escala de -1 a 1. Pegar en el borde izquierdo da -1, el centro exacto da 0, el borde derecha da 1
#vel_x = offset * MAX_VEL_X traduce eso directamente en velocidad horizontal: cuanto más borde, más abierto sale el rebote
#vel_y = -max(MIN_VEL_Y, 8 - abs(vel_x)) hace que, cuando vel_x es grande (pegó cerca del borde), vel_y se achique un poco
#para que el rebote se sienta más de costado, pero nunca por debajo de MIN_VEL_Y, asó evitás que la pelota salga tan horizontal que rebote ternamente
#entre pared y paleta sin nunca subir lo suficiente