from typing import Any
import pygame
import math
import random
import constantes

from pygame.sprite import Group

class Weapon():
    def __init__(self, image, imagen_bala):
        self.imagen_bala = imagen_bala
        self.imagen_original = image
        self.angulo = 0
        self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo)
        self.forma = self.imagen.get_rect()
        self.disparada = False
        self.ultimo_disparo = pygame.time.get_ticks()
    
    
    def update(self, personaje):
        disparo_cooldown = constantes.COOLDOWN_BALAS
        bala = None
        self.forma.center = personaje.forma.center
        
        if personaje.flip == False:
            self.forma.x = self.forma.x + personaje.forma.width/4
            self.rotar_arma(False)
            
        if personaje.flip == True:
            self.forma.x =self.forma.x - personaje.forma.width/4
            self.rotar_arma(True)
            
        #Mover la pistola con el mouse
        mouse_pos = pygame.mouse.get_pos()
        
        distancia_x = mouse_pos[0] - self.forma.centerx
        
        distancia_y = -(mouse_pos[1] - self.forma.centery)
        
        self.angulo = math.degrees(math.atan2(distancia_y, distancia_x))
        
        self.forma.y = self.forma.y + 11
        
        #print(self.angulo)
        
        
        #Detectar lso click del mouse
        
        if pygame.mouse.get_pressed()[0] and self.disparada == False and (pygame.time.get_ticks()-self.ultimo_disparo >= disparo_cooldown):            
            bala = Bullet(self.imagen_bala, self.forma.centerx, self.forma.centery, self.angulo)
            self.disparada = True
            self.ultimo_disparo = pygame.time.get_ticks()
            
            
        #Resetear el click del mouse
        if pygame.mouse.get_pressed()[0] == False:
            self.disparada = False
        return bala
    
    def rotar_arma(self, rotar):
        
        if rotar == True:            
            imagen_flip = pygame.transform.flip(self.imagen_original, True, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)
            
        else: 
            imagen_flip = pygame.transform.flip(self.imagen_original, False, False )
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)
        
    def dibujar(self, interfaz):
        self.imagen = pygame.transform.rotate(self.imagen, self.angulo)
        interfaz.blit(self.imagen, self.forma)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.imagen_original = image
        self.angulo = angle
        self.image = pygame.transform.rotate(self.imagen_original,self.angulo)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        #Velocidad de bala
        self.delta_x = math.cos(math.radians(self.angulo)) * constantes.VELOCIDAD_BALA
        self.delta_y = -math.sin(math.radians(self.angulo)) * constantes.VELOCIDAD_BALA
    
    def update(self, lista_enemigos):
        daño = 0
        pos_daño = None
        self.rect.x += self.delta_x
        self.rect.y = self.rect.y + self.delta_y
        
        #Ver si las balas salieron de pantalla
        if self.rect.right < 0 or self.rect.left > constantes.ANCHO_VENTANA or self.rect.bottom < 0 or self.rect.top > constantes.ALTO_VENTANA:
            self.kill()
        
        # Verificar si hay colision con enemigos
        for enemigo in lista_enemigos:
            if enemigo.forma.colliderect(self.rect):
                daño = 15 + random.randint(-7, 7)
                pos_daño = enemigo.forma
                enemigo.energia -= daño
                self.kill()
                break
        return daño, pos_daño
    def dibujar(self, interfaz):
        interfaz.blit(self.image, (self.rect.centerx, self.rect.centery - int(self.image.get_height()/2)))