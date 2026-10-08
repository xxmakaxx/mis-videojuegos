import sys
import pygame

pygame.init()

ANCHO,ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO,ALTO))
reloj = pygame.time.Clock()

GRAVEDAD = 0.5
VEL_MOV = 6
FUERZA_SALTO = -13
VIDAS_INICIALES = 3
INVULNERABLE_MS = 1500

mono = pygame.Rect(100, 300, 40, 40)
vel_x, vel_y = 0, 0
en_piso = False

plataformas = [
    pygame.Rect(0, ALTO - 40, ANCHO, 40), #Piso
    pygame.Rect(200, 450, 180, 25),
    pygame.Rect(450, 360, 180, 25),
    pygame.Rect(600, 250, 180, 25),
]

def crear_bananas():
    return [
        pygame.Rect(250, 420, 20, 20),
        pygame.Rect(500, 330, 20, 20),
        pygame.Rect(650, 220, 20, 20),
    ]

def crear_enemigos():
    return [
        {"rect": pygame.Rect(200, 420, 30, 30), "vel": 2, "min": 200, "max": 380},
        {"rect": pygame.Rect(450, 330, 30, 30), "vel": -2, "min": 450, "max": 630},
        {"rect": pygame.Rect(300, 530, 30, 30), "vel": 3, "min": 300, "max": 700}, 
    ]

bananas = crear_bananas()
enemigos = crear_enemigos()

juntas = 0

vidas = VIDAS_INICIALES
ultimo_golpe = -INVULNERABLE_MS

inicio = pygame.time.get_ticks()

fuente = pygame.font.SysFont(None, 36)

ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and en_piso:
                vel_y = FUERZA_SALTO

    #Movimiento horitontal
    teclas = pygame.key.get_pressed()
    vel_x = (teclas[pygame.K_RIGHT] - teclas[pygame.K_LEFT]) * VEL_MOV

    #Gravedad y movimiento
    vel_y += GRAVEDAD
    mono.x += vel_x
    mono.y += vel_y

    #Colisión con plataformas
    en_piso = False
    for p in plataformas:
        if mono.colliderect(p) and vel_y > 0 and mono.bottom <= p.top + 15:
            mono.bottom = p.top
            vel_y = 0
            en_piso = True

    #Juntas bananas
    for b in bananas[:]:
        if mono.colliderect(b):
            bananas.remove(b)
            juntas += 1

    #Mover enemigos
    for e in enemigos:
        e["rect"].x += e["vel"]
        if e["rect"].left < e["min"] or e["rect"].right > e["max"]:
            e["vel"] *= -1

    #Colisión con enemigos
    ahora = pygame.time.get_ticks()
    invulnerable = ahora - ultimo_golpe < INVULNERABLE_MS
    if not invulnerable:
        for e in enemigos:
            if mono.colliderect(e["rect"]):
                vidas -= 1
                ultimo_golpe = ahora
                vel_y = -8 #pequeño rebote
                break

    #Sin vidas: final del juego
    if vidas <= 0:
        print("¡Game Over! Te quedaste sin vidas.")
        ejecutando = False

    #Si el mono se cae de la pantalla, reiniciar
    if mono.top > ALTO:
        mono.x, mono.y = 100, 300
        vel_x, vel_y = 0, 0
        juntas = 0
        bananas = crear_bananas()
        enemigos = crear_enemigos()
        vidas = VIDAS_INICIALES
        inicio = pygame.time.get_ticks()

    #Dibujar
    segundos = (pygame.time.get_ticks() - inicio) // 1000
    pantalla.fill((150, 210, 255))
    for p in plataformas:
        pygame.draw.rect(pantalla, (90, 60, 30), p)
    for e in enemigos:
        pygame.draw.rect(pantalla, (200, 40, 40), e["rect"])
    if not invulnerable or (ahora // 100) % 2 == 0:  # Parpadeo cuando es invulnerable
        pygame.draw.rect(pantalla, (160, 110, 50), mono)
    for b in bananas:
        pygame.draw.circle(pantalla, (255, 220, 60), b.center, 10)

    texto = fuente.render(f"Tiempo: {segundos}s", True, (0, 0, 0))
    pantalla.blit(texto, (10, 10))
    texto_vidas = fuente.render(f"Vidas: {vidas}", True, (0, 0, 0))
    pantalla.blit(texto_vidas, (10, 40))
    pygame.display.set_caption(f"El Mono - Bananas: {juntas} - Tiempo: {segundos}s")
    pygame.display.flip()
    reloj.tick(60)

    if len(bananas) == 0:
        print(f"¡Juntaste todas las bananas en {segundos} segundos!")
        ejecutando = False

pygame.quit()
sys.exit()