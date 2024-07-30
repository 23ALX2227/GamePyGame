import pygame
import constantes
from personaje import Personaje
from weapon import Weapon
from textos import Damagetext
import os

#Funciones:
#Escalar imagenes
def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image, (w*scale, h*scale))
    return nueva_imagen

#Funcion para contar elelemntos
def contar_elementos(directorio):
    return len(os.listdir(directorio))


#Funcionlistar nombre elementos
def nombres_carpetas(directorio):
    return os.listdir(directorio)


pygame.init()

ventana = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))

pygame.display.set_caption("Juego en Pygame")

# Fuentes

font = pygame.font.Font("./aseets/fonts/monogram.ttf", 25)

# Importar imagenes
# Energia
corazon_vacio = pygame.image.load("./aseets/images/items/heart_empty.png").convert_alpha()
corazon_vacio = escalar_img(corazon_vacio, constantes.SCALA_CORAZON)
corazon_mitad = pygame.image.load("./aseets/images/items/heart_half.png").convert_alpha()
corazon_mitad = escalar_img(corazon_mitad, constantes.SCALA_CORAZON)
corazon_lleno = pygame.image.load("./aseets/images/items/heart_full.png").convert_alpha()
corazon_lleno = escalar_img(corazon_lleno, constantes.SCALA_CORAZON)

# Personaje

animaciones = []
for i in range (7):
    img = pygame.image.load(f"./aseets/images/characters/player/Player_{i}.png")
    img = escalar_img(img, constantes.SCALA_PERSONAJE)
    animaciones.append(img)
    
# Enemigos
directorio_enemigos = "./aseets/images/characters/enemies"
tipo_enemigos = nombres_carpetas(directorio_enemigos)

animaciones_enemigos = []

for eni in tipo_enemigos:    
    lista_temp = []
    ruta_temp = f"./aseets/images/characters/enemies/{eni}"
    num_animaciones = contar_elementos(ruta_temp)
    
    for i in range(num_animaciones):        
        img_enemigo = pygame.image.load(f"{ruta_temp}/{eni}_{i + 1}.png").convert_alpha()
        img_enemigo = escalar_img(img_enemigo, constantes.SCALA_ENEMIGO)
        lista_temp.append(img_enemigo)
        
    animaciones_enemigos.append(lista_temp)


# Arma
imagen_pistola = pygame.image.load(f"./aseets/images/weapons/gun.png").convert_alpha()
imagen_pistola = escalar_img(imagen_pistola, constantes.SCALA_ARMA)

# Balas 
imagen_balas = pygame.image.load(f"./aseets/images/weapons/bullet.png").convert_alpha()
imagen_balas = escalar_img(imagen_balas, constantes.SCALA_BALA)

def vida_jugador():
    c_mitad_dibujado = False
    for i in range(3):
        if jugador.energia >= ((i+1)*25):
            ventana.blit(corazon_lleno, (5+1*50, 5))
        elif jugador.energia % 25 > 0 and c_mitad_dibujado == False:
            ventana.blit(corazon_mitad, (5+i*50, 5))
            c_mitad_dibujado = True
        else:
            ventana.blit(corazon_vacio, (5 + i * 50, 5))

# Crea un jugador de la clase personaje
jugador = Personaje(50, 50, animaciones,100)

# Crea un enemigo de la clase personaje
goblin_1 = Personaje(400, 300, animaciones_enemigos[0], 100)
goblin_2 = Personaje(100, 250, animaciones_enemigos[0], 100)   
honguito_1 = Personaje(200, 200, animaciones_enemigos[1], 100)

# Crear lista de enemigos
lista_enemigos = []
lista_enemigos.append(goblin_1)
lista_enemigos.append(goblin_2)
lista_enemigos.append(honguito_1)

# Crear arma 
pistola = Weapon(imagen_pistola, imagen_balas)

# Crear un grupo de sprites
grupo_damage_text = pygame.sprite.Group()
grupo_balas = pygame.sprite.Group()


# Variables de movimiento
mover_arriba = False
mover_abajo = False
mover_izquierda = False
mover_derecha = False

reloj = pygame.time.Clock()

run = True

while run:
    
    reloj.tick(constantes.FPS)
    
    ventana.fill(constantes.COLOR_BG)
    
    # Movimiento del jugador
    delta_x = 0
    delta_y = 0
    
    if mover_derecha == True:
        delta_x = constantes.VELOCIDAD        
    if mover_izquierda == True:
        delta_x = -constantes.VELOCIDAD
    if mover_arriba == True:
        delta_y = -constantes.VELOCIDAD
    if mover_abajo == True:
        delta_y = constantes.VELOCIDAD
    
    # MOver al jugador
    jugador.movimiento(delta_x, delta_y)
    
    # Actualiza estado del jugdor
    jugador.update()
    
    # Actualiza estado del enemigo
    for ene in lista_enemigos:
        ene.update()
        print(ene.energia)
    
    # Actuliza el estado del arma
    bala = pistola.update(jugador) 
    
    if bala:
        grupo_balas.add(bala)
    for bala in grupo_balas:
        damage, pos_damage = bala.update(lista_enemigos)
        
        if damage:
            damage_text = Damagetext(pos_damage.centerx, pos_damage.centery, str(damage), font, constantes.ROJO)
            grupo_damage_text.add(damage_text)
    # Actualizar daño
    grupo_damage_text.update()
    
    # Dibuja al jugador
    jugador.dibujar(ventana)
    
    # Dibuja al enemigo
    for ene in lista_enemigos:
        ene.dibujar(ventana)
    
    # Dibijar el arma
    pistola.dibujar(ventana)
    
    # Dibujar balas
    for bala in grupo_balas:
        bala.dibujar(ventana)
        
    # Dibujar los corazones
    vida_jugador()    
    
    # Dibujar textos
    grupo_damage_text.draw(ventana)
        
    
    for event in pygame.event.get():
        #Para cerrar el juego
        if event.type == pygame.QUIT:
            run = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                mover_izquierda = True
            if event.key == pygame.K_d:
                mover_derecha = True
            if event.key == pygame.K_w:
                mover_arriba = True
            if event.key == pygame.K_s:
                mover_abajo = True
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                mover_izquierda = False
            if event.key == pygame.K_d:
                mover_derecha = False
            if event.key == pygame.K_w:
                mover_arriba = False
            if event.key == pygame.K_s:
                mover_abajo = False

    pygame.display.update()

pygame.quit()


