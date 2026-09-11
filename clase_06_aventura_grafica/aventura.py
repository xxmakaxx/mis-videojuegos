import sys
import pygame

pygame.init()

ANCHO, ALTO = 900, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("arial", 26)

# -- INVENTARIO: objetos que tiene el jugador --
inventario = {
    "banana" : True,
}

# -- FONDOS: color de fondo según la escena --
fondos = {
    "inicio": (20, 45, 20), #Bosque: verde
    "cueva": (45, 38, 30), #Cueva: marrón oscuro
    "mono": (45, 38, 30), #Sigue dentro de la cueva
    "cofre": (55, 40, 20), #Cueva con el cofre: marrón dorado
    "tesoro": (70, 55, 15), #Brillo del tesoro: dorado oscuro
    "rio": (15, 35, 60), #Río: azul
    "cascada": (10, 50, 70), #Cascada: azul más intenso
}

# -- HISTORIA: completá los textos que faltan --
historia = {
    "inicio": {
        "texto": "Estás en la selva. Escuchás un ruido entre los árboles.", 
        "opciones": [("Ir a investigar", "cueva"), ("Seguir el sendero", "rio")],
    }, 
    "cueva": {
        "texto": "Dentro de la cueva hay un cofre dorado. Un mono lo cuestodia.",
        "opciones": [("Hablar con el mono", "mono"), ("Abrir el cofre a escondidas", "cofre")],
    },
    "mono": {
        "texto": "El monmo habla: 'Dame una banana y el tesoro será tuyo!'",
        #El tercer valor de la tupla es el objeto requerido
        "opciones": [("Dar la banana", "tesoro", "banana"), ("Negarme", "inicio")],
    },
    "tesoro": {
        "texto": "Ganaste el tesoro legendario de la selva! Fin de la aventura.",
        "opciones":[],
    },
    "rio": {
        "texto": "El río es muy ancho y no hay puente. No podés cruzar.",
        "opciones": [("Volver al inicio", "inicio"), ("Seguir el río", "cascada")],
    },
    "cascada": {
        "texto": "Llegaste a una cascada. El agua es muy fuerte y te arrastra.",
        "opciones": [("Volver al inicio", "inicio")],
    },
    "cofre": {
        "texto": "El cofre estaba lleno de oro! Pero el mono se enoja y te persigue.",
        "opciones": [("Correr", "inicio"), ("Luchar con el mono", "mono")],
    }
}

escena = "inicio"

def opciones_disponibles(opciones):
    #Filtra las opciones según lo que haya en el inventario
    disponibles = []
    for opcion in opciones:
        texto, destino = opcion[0], opcion[1]
        requisito = opcion[2] if len(opcion) > 2 else None
        if requisito is None or inventario.get(requisito, False):
            disponibles.append((texto, destino, requisito))
    return disponibles

def dibujar_botones(opciones):
    botones = []
    y = ALTO - 40 * len(opciones) - 20
    for texto, destino, requisito in opciones:
        rect = pygame.Rect(ANCHO // 2 - 200, y, 400, 34)
        pygame.draw.rect(pantalla, (60, 60, 130), rect)
        pantalla.blit(fuente.render(texto, True, (255, 255, 255)), (rect.x + 12, rect.y + 6))
        botones.append((rect, texto, destino, requisito))
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
        pantalla.blit(fuente.render(linea, True, (255, 255, 255)), (80, y))
        y += 34

ejecutando = True
while ejecutando:
    opciones = opciones_disponibles(historia[escena]["opciones"])

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN and opciones:
            mx, my = pygame.mouse.get_pos()
            pantalla.fill(fondos.get(escena, (20, 30, 20))) #Recalcular rects con el color correcto
            botones = dibujar_botones(opciones)
            for rect, texto, destino, requisito in botones:
                if rect.collidepoint(mx, my):
                    #Si la opción consume el objeto, lo sacamos del inventario
                    if requisito:
                        inventario[requisito] = False
                    escena = destino
                    if not historia[escena]["opciones"]:
                        print("La aventura terminó.")
                    break

    pantalla.fill(fondos.get(escena, (20, 30, 20)))
    pantalla.blit(fuente.render("AVENTURA EN LA SELVA", True, (255, 200, 60)), (80, 60))
    dibujar_texto(historia[escena]["texto"])
    dibujar_botones(opciones)
    pygame.display.flip()
    reloj.tick(20)

pygame.quit()
sys.exit()