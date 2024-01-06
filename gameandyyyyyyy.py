import pygame
import random
import sys

# Inicialización de Pygame
pygame.init()

# Definición de colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

# Configuración de la pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pistolero vs Zombis")

# Cargar imágenes
imagen_pistolero = pygame.image.load("pistolero.png")  
imagen_zombi = pygame.image.load("zombifs.png")  
imagen_bala = pygame.image.load("bala.png")  

# Escalado de imágenes
imagen_pistolero = pygame.transform.scale(imagen_pistolero, (50, 50))
imagen_zombi = pygame.transform.scale(imagen_zombi, (50, 50))
imagen_bala = pygame.transform.scale(imagen_bala, (10, 10))

# Clases
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = imagen_pistolero
        self.rect = self.image.get_rect()
        self.rect.center = (ANCHO // 2, ALTO - 50)
        self.velocidad = 5

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.velocidad

class Zombi(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = imagen_zombi
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.velocidad = random.randint(1, 3)

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.top > ALTO + 10:
            self.rect.x = random.randrange(ANCHO - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.velocidad = random.randint(1, 3)

class Bala(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = imagen_bala
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()

# Grupo de sprites
todos_los_sprites = pygame.sprite.Group()
jugador = Jugador()
todos_los_sprites.add(jugador)

zombis = pygame.sprite.Group()
balas = pygame.sprite.Group()

for i in range(10):
    zombi = Zombi()
    todos_los_sprites.add(zombi)
    zombis.add(zombi)

# Puntuación
puntuacion = 0

# Reloj para controlar la velocidad de actualización
reloj = pygame.time.Clock()

# Fuente para mostrar la puntuación
fuente = pygame.font.Font(None, 36)

# Bucle principal del juego
jugando = True
while jugando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  
            bala = Bala()
            bala.rect.center = jugador.rect.center
            todos_los_sprites.add(bala)
            balas.add(bala)

    # Actualizar
    todos_los_sprites.update()

    # Verificar colisiones de balas con zombis
    impactos = pygame.sprite.groupcollide(balas, zombis, True, True)
    for impacto in impactos:
        puntuacion += 1
        zombi = Zombi()
        todos_los_sprites.add(zombi)
        zombis.add(zombi)

    # Verificar colisiones de zombis con el jugador
    colisiones = pygame.sprite.spritecollide(jugador, zombis, True)
    for colision in colisiones:
        jugando = False

    # Renderizar
    pantalla.fill(NEGRO)
    todos_los_sprites.draw(pantalla)

    # Mostrar puntuación en la pantalla
    texto_puntuacion = fuente.render("Puntuación: {}".format(puntuacion), True, BLANCO)
    pantalla.blit(texto_puntuacion, (10, 10))

    # Actualizar pantalla
    pygame.display.flip()

    # Controlar la velocidad de actualización
    reloj.tick(60)

# Mostrar mensaje de puntuación
mensaje = fuente.render("¡Tu puntuación es: {}!".format(puntuacion), True, BLANCO)
pantalla.blit(mensaje, (ANCHO // 2 - 150, ALTO // 2 - 20))
pygame.display.flip()

# Esperar unos segundos antes de salir
pygame.time.delay(3000)

# Salir del juego
pygame.quit()
sys.exit()
