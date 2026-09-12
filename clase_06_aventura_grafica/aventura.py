import sys
import pygame
import os

pygame.init()
pygame.mixer.init()

#Ubicación del archivo py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#Carpeta imágenes, que esta al lado del archivo py
CARPETA_IMAGENES = os.path.join(BASE_DIR, "imagenes")

CARPETA_SONIDOS = os.path.join(BASE_DIR, "sonidos")

ANCHO, ALTO = 900, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("arial", 26)

# -- INVENTARIO: objetos que tiene el jugador --
inventario = {
    "banana" : True,
}

# -- VIDAS: cuantás desiciones malas puede tolerar el jugador --
VIDAS_INICIALES = 3
vidas = VIDAS_INICIALES

# -- AVISO: mensaje temporal que se muestra al perder una vida --
FPS = 20 
DURACION_AVISO_SEGUNDOS = 2
aviso_texto = ""
aviso_frames_restantes = 0 #Mientras sea mayor a 0, el aviso se sigue mostrando

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

# -- IMAGENES: una por escena
def cargar_imagen(nombre_archivo):
    ruta = os.path.join(CARPETA_IMAGENES, nombre_archivo)

    try:
        img = pygame.image.load(ruta).convert()
        return pygame.transform.scale(img, (ANCHO, ALTO))
    except (pygame.error, FileNotFoundError):
        print(f"No se pudo cargar {ruta}, se usará color de fondo.")
        return None

imagenes = {
    "inicio": cargar_imagen("bosque.png"),
    "cueva": cargar_imagen("cueva.png"),
    "mono": cargar_imagen("cueva.png"),
    "cofre": cargar_imagen("cofre.png"),
    "tesoro": cargar_imagen("tesoro.png"),
    "rio": cargar_imagen("rio.png"),
    "cascada": cargar_imagen("cascada.png"),
}

# -- SONIDOS: efectos que se reproducen al elegir opciones
def cargar_sonido(nombre_archivo):
    ruta = os.path.join(CARPETA_SONIDOS, nombre_archivo)

    try:
        return pygame.mixer.Sound(ruta)
    except(pygame.error, FileNotFoundError):
        print(f"No se pudo cargar el sonido {ruta}, se continuará sin sonido.")
        return None

#Sonido genérico al elegir cualquier opción
sonido_click = cargar_sonido("click.mp3")

#Sonidos especiales según a dónde lleve la opción elegida
sonidos_por_escena = {
    "tesoro": cargar_sonido("victory.wav"),
    "cascada": cargar_sonido("waterfall.mp3"),
    "mono": cargar_sonido("monkey.wav"),
}

duracion_maxima = {
    "cascada": 1500, #Cortar el sonido de la cascada a 1.5 segundos
}

def reproducir_sonido(destino):
    #Reproduce el sonido genérico de click y, si existe, uno especial para al escena destino
    if sonido_click:
        sonido_click.play()
    sonido_especial = sonidos_por_escena.get(destino)
    if sonido_especial:
        limite_ms = duracion_maxima.get(destino, 0)
        sonido_especial.play(maxtime=limite_ms)


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
        "texto": "El mono habla: 'Dame una banana y el tesoro será tuyo!'",
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
        "dano": 1, #Decisión mala: perdés una vida
    },
    "cofre": {
        "texto": "El cofre estaba lleno de oro! Pero el mono se enoja y te persigue.",
        "opciones": [("Correr", "inicio"), ("Luchar con el mono", "mono")],
        "dano": 1
    },
    "fin_vidas": {
        "texto": "Te quedaste sin vidas. La selva fue demasiado para vos. Fin de la aventura.",
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

def dibujar_fondo(escena):
    #Dibuja la imagen de la escena si existe; si no, usa el color de "fondos"
    imagen = imagenes.get(escena)
    if imagen:
        pantalla.blit(imagen, (0, 0))
    else:
        pantalla.fill(fondos.get(escena, (20, 30, 20)))

def dibujar_vidas():
    texto_vidas = f"Vidas: {vidas}"
    superficie = fuente.render(texto_vidas, True, (255, 90, 90))
    pantalla.blit(superficie, (ANCHO - superficie.get_width() - 20, 20))

def dibujar_aviso():
    if aviso_frames_restantes > 0:
        superficie = fuente.render(aviso_texto, True, (255, 60, 60))
        rect = superficie.get_rect(center=(ANCHO // 2, 110))
        pantalla.blit(superficie, rect)

ejecutando = True
while ejecutando:
    opciones = opciones_disponibles(historia[escena]["opciones"])

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN and opciones:
            mx, my = pygame.mouse.get_pos()
            dibujar_fondo(escena)
            botones = dibujar_botones(opciones)
            for rect, texto, destino, requisito in botones:
                if rect.collidepoint(mx, my):
                    reproducir_sonido(destino)
                    #Si la opción consume el objeto, lo sacamos del inventario
                    if requisito:
                        inventario[requisito] = False
                    escena = destino
                    aviso_frames_restantes = 0
                    dano = historia[escena].get("dano", 0)
                    if dano:
                        vidas -= dano
                    aviso_texto = "Perdiste una vida!"
                    aviso_frames_restantes = FPS * DURACION_AVISO_SEGUNDOS
                    if vidas <= 0:
                        vidas = 0
                        escena = "fin_vidas"
                    if not historia[escena]["opciones"]:
                        print("La aventura terminó.")
                    break

    dibujar_fondo(escena)
    pantalla.blit(fuente.render("AVENTURA EN LA SELVA", True, (255, 200, 60)), (80, 60))
    dibujar_vidas()
    dibujar_aviso()
    dibujar_texto(historia[escena]["texto"])
    dibujar_botones(opciones)
    pygame.display.flip()
    reloj.tick(FPS)

    if aviso_frames_restantes > 0:
        aviso_frames_restantes -= 1

pygame.quit()
sys.exit()