import sys
import pygame
pygame.init()

ANCHO, ALTO = 900, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("arial", 26)

# -- INVENTARIO: objetos que tiene el jugador --
inventario = {
    "llave": False, #Todavía no la encontraste
}

# -- FONDOS: color de fondo según la escena --
fondos = {
    "inicio": (35, 45, 60),
    "cubierta": (35, 45, 60),
    "bodega": (40, 32, 22),
    "loro": (35, 45, 60),
    "camarote": (55, 40, 25),
    "motin": (60, 20, 20),
    "tesoro": (80, 65, 15),
    "calabozo": (15, 15, 18),
}

# -- HISTORIA: aventura en un barco pirata --
historia = {
    "inicio": {
        "texto": "Despertás en la cubierta de un barco pirata, en plena tormenta. No recordás cómo llegaste ahí.",
        "opciones": [("Explorar la cubierta", "cubierta"), ("Bajar a la bodega", "bodega")],
    },
    "cubierta": {
        "texto": "El viento silba entre las velas rotas. Un loro te observa parada en el mástil principal.",
        "opciones": [("Hablar con el loro", "loro"), ("Ir al camarote del capitán", "camarote")],
    },
    "bodega": {
        "texto": "Entre barriles viejos y cajas rotas, encontrás una llave oxidada. Al se mueve en la oscuridad.",
        #El cuarto valor de la tupla es el objeto que se OTORGA al elegir esa opción
        "opciones": [
            ("Tomar la llave y subir", "cubierta", None, "llave"),
            ("Enfrentar lo que se mueve en la oscuridad", "motin"),
        ],
    },
    "loro": {
        "texto": "El loro grazna: 'El mapa está en el camarote! Pero la puerta... está cerrada con llave!'",
        "opciones": [("Volver a la cubierta", "cubierta"), ("Ir al camarote del capitán", "camarote")],
    },
    "camarote": {
        "texto": "Frente a vos, la puerta del camarote del capitán está firmemente cerrada.",
        "opciones": [
            ("Abrir la puerta con la llave", "tesoro", "llave"),
            ("Forzar la puerta a patadas", "motin"),
        ],
    },
    "motin": {
        "texto": "El ruido alertó a la tripulación amotinada. Te rodean antes de que puedas escapar.",
        "opciones": [("Aceptar tu destino", "calabozo")],
    },
    "tesoro": {
        "texto": "Dentro del camarote encontrás el mapa y el cofre del Capitán Barbanegra. Sos rico! Fin de la aventura.",
        "opciones": [], 
    },
    "calabozo": {
        "texto": "Te encierran en el calabozo del barco. Ahí termina tu aventura, prisionera para siempre.",
        "opciones": [], 
    },
}

escena = "inicio"

def opciones_disponibles(opciones):
    #Filtra las opciones según lo que haya en el inventario
    disponibles = []
    for opcion in opciones:
        texto, destino = opcion[0], opcion[1]
        requisito = opcion[2] if len(opcion) > 2 else None
        otorga = opcion[3] if len(opcion) > 3 else None
        if requisito is None or inventario.get(requisito, False):
            disponibles.append((texto, destino, requisito, otorga))
    return disponibles

def dibujar_botones(opciones):
    botones = []
    y = ALTO - 40 * len(opciones) - 20
    for texto, destino, requisito, otorga in opciones:
        rect = pygame.Rect(ANCHO // 2 - 200, y, 400, 34)
        pygame.draw.rect(pantalla, (60, 60, 130), rect)
        pantalla.blit(fuente.render(texto, True, (255, 255, 255)), (rect.x + 12, rect.y + 6))
        botones.append((rect, texto, destino, requisito, otorga))
        y += 44
    return botones

def dibujar_texto(texto, limite=45):
    palabras = texto.split()
    lineas, actual = [], ""
    for p in palabras: 
        if len(actual) + len(p) + 1 > limite:
            lineas.append(actual)
            actual = p
        else:
            actual = actual + " " + p
    lineas.append(actual)
    y = 150
    for linea in lineas:
        pantalla.blit(fuente.render(linea, True, (255, 255, 255)),(80, y))
        y += 34

ejecutando = True
while ejecutando:
    opciones = opciones_disponibles(historia[escena]["opciones"])

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN and opciones:
            mx, my = pygame.mouse.get_pos()
            pantalla.fill(fondos.get(escena, (20, 30, 20)))
            botones = dibujar_botones(opciones)
            for rect, texto, destino, requisito, otorga in botones:
                if rect.collidepoint(mx, my):
                    #Si la opción consume el objeto, lo sacamos del inventario
                    if requisito:
                        inventario[requisito] = False
                    #Si la opción otorga un objeto, lo sumamos al inventario
                    if otorga:
                        inventario[otorga] = True
                    escena = destino
                    if not historia[escena]["opciones"]:
                        print("La aventura terminó.")
                    break

    pantalla.fill(fondos.get(escena, (20, 30, 20)))
    pantalla.blit(fuente.render("AVENTURA PIRATA", True, (255, 200, 60)), (80, 60))
    dibujar_texto(historia[escena]["texto"])
    dibujar_botones(opciones)
    pygame.display.flip()
    reloj.tick(20)

pygame.quit()
sys.exit()
