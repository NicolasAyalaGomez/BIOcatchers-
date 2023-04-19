import sys
import pygame

class Mapa():
    def __init__(self, screen):
        # Carga las imagenes y las guarda en atributos
        self.mapa = pygame.image.load("Mapa sprites/mapa_niveles.png") 
        self.cristo = pygame.image.load("Mapa sprites/nivel1_cristo.png")
        self.pinSprite = pygame.image.load("Mapa sprites/levelPin.png")

        # establece el alpha en 0 para que la imagen se vuelva completamente transparente
        self.cristo.set_alpha(0)

        # guarda la ventana para poder dibujar sobre ella luego
        self.screen = screen
        
        # lista de pines del mapa, contiene la posicion en la que se encuentra el pin en el mapa, y booleanos
        # para saber si se paso el nivel y de esa manera saber si mostrar o no el pin en el mapa
        self.Pines = [
            [(357,192),False, False, (0,0)],
            [(0,0),False, False, (0,0)],
            [(0,0),False, False, (0,0)],
            [(0,0),False, False, (0,0)],
            [(0,0),False, False, (0,0)],
            [(0,0),False, False, (0,0)]
        ]
    
    # metodo para dibujar el mapa con sus elementos y 
    def Mostrar(self, player):

        # ------------------------------------------ variables ------------------------------------------ 

        # variable para controlar el bucle while y salir
        #  de el cuando se presione espacio en el mapa
        done = True
        
        # silencia la musica con fadeout (la quita poco
        # a poco en un intervalo de 500 milisegundos) 
        pygame.mixer.music.fadeout(500)
        
        # reloj para llevar el control de fps
        clock = pygame.time.Clock()   

        # obtiene el tiempo actual. Sirve para saber
        # que tanto tiempo paso desde que se inició 
        # el bucle while
        time = pygame.time.get_ticks()
        
        # Bucle while
        while done:
            
            # recorre la lista de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # si se presiono el boton de salir 
                    pygame.quit() # termina pygame
                    sys.exit() # termina el programa

                if event.type == pygame.KEYDOWN: # si se presiona una tecla
                    if event.key == pygame.K_SPACE: # si la tecla es espacio
                        done = False # establece done en False para que se salga del bucle while y continue con el juego

            if self.Pines[0][1]: # si el pin se activó (porque se pasó el nivel)
                esperado = self.Pines[0][0] # le asigna posicion al pin (la posicion en la que deberia de estar en el mapa)
            else:# si no se activó (porque no ha pasado el nivel)
                esperado = (0,-100) # le asigna una posicion fuera de la pantalla para que no se muestre el pin
                
            # esta linea sirve para mover poco a poco el pin hsata la posicion esperada
            # de manera suave y progresiva
            self.Pines[0][3]=(self.Pines[0][3][0]+(esperado[0]-self.Pines[0][3][0])*0.1, self.Pines[0][3][1]+(esperado[1]-self.Pines[0][3][1])*0.1)

            # si ya pasaron 500 milisegundos desde que se abrió el mapa y el cristo aun no es totalmente visible
            # y ademas el pin 1 ya se mostró (porque ya se pasó el nivel)
            # entonces va aumentando el alpha del cristo para que vaya apareciendo poco a poco            
            if(pygame.time.get_ticks()-time>800 and self.cristo.get_alpha()<255 and self.Pines[0][1]):
                self.cristo.set_alpha(self.cristo.get_alpha()+10)
                
            

            # dibuja los elementos del mapa en la pantalla
            self.screen.blit(self.mapa, (0,0))
            self.screen.blit(self.cristo, (0,0))
            self.screen.blit(self.pinSprite, (self.Pines[0][3][0]-self.pinSprite.get_width()//2, self.Pines[0][3][1]-self.pinSprite.get_height()//2))
            
            # actualiza los mensajes mostrados en pantalla (en caso de que haya)
            player.updateMess()

            # Actualiza la pantalla para mostrar las ultimas modificaciones
            pygame.display.update()
            # controla los fps para que se mantengan en 60
            clock.tick(60)
            