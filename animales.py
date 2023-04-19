from spritesheet_functions import SpriteSheet
import pygame
import constants
from math import sqrt
from platforms import MovingPlatform

from copy import deepcopy

from random import randint

def distancia_euclidiana(x1, y1, x2, y2):
    distancia = sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distancia

class Animal(pygame.sprite.Sprite):

    antpos = 0

    change_x = 0
    change_y = 0

    walking_frames_l = []
    walking_frames_r = []

    idle_frames_l = []
    idle_frames_r = []

    tarjetaImage = None

    level = None

    direction = "SR"

    rapidez = 4

    player = None

    screen = None

    collR = False
    collL = False


    randMovingTime = 0
    randMovingTimeInit = 0

    def __init__(self, dir_SpriteSheets, dir_Tarjeta, screen, recortar = False):
        """ En dir_SpriteSheets recibe un arreglo con dos 
            direcciones correspondientes al walking y al 
            Idle del animal                               """
        pygame.sprite.Sprite.__init__(self)
        self.dir_SpriteSheetW =  dir_SpriteSheets[0]
        self.dir_SpriteSheetI =  dir_SpriteSheets[1]
        self.dir_Tarjeta = dir_Tarjeta

        self.screen = screen

        sprite_sheet = SpriteSheet(self.dir_SpriteSheetW)
        sprite_sheet.scaled_sprite(1/11)
        w,h = sprite_sheet.getSize()
        wS = w//4
        for i in range(4):
            image = sprite_sheet.get_image(i*wS, 5 if recortar else 0, wS, h)
            self.walking_frames_r.append(image)
            image = pygame.transform.flip(image, True, False)
            self.walking_frames_l.append(image)
        
        sprite_sheet = SpriteSheet(self.dir_SpriteSheetI)
        sprite_sheet.scaled_sprite(1/11)
        w,h = sprite_sheet.getSize()
        wS = w//4
        for i in range(4):
            image = sprite_sheet.get_image(i*wS, 0, wS, h)
            self.idle_frames_r.append(image)
            image = pygame.transform.flip(image, True, False)
            self.idle_frames_l.append(image)

        self.image = self.idle_frames_r[0]
        self.rect = self.image.get_rect()

        """sirve para cambiar de frame en la animacion de idle cada cierto tiempo"""
        self.sepFrameTime = 0
        self.frameIdle = 0
    def update(self):
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x
        pos = self.rect.x + self.level.world_shift
        if(pygame.time.get_ticks()-self.sepFrameTime>100):
            if self.frameIdle<3:
                if pos!=self.antpos or "S" in self.direction:
                    self.frameIdle+=1
            else:
                self.frameIdle=0
            self.sepFrameTime = pygame.time.get_ticks()
        if self.direction == "SR":
            self.image = self.idle_frames_r[self.frameIdle]
        elif self.direction == "SL":
            self.image = self.idle_frames_l[self.frameIdle]
        elif self.direction == "R":
            self.image = self.walking_frames_r[self.frameIdle]
        elif self.direction == "L":
            self.image = self.walking_frames_l[self.frameIdle]
        self.antpos = pos
        
        # if self.direction == "R":
        #     frame = (pos // 30) % len(self.walking_frames_r)
        #     self.image = self.walking_frames_r[frame]
        # elif self.direction == "L":
        #     frame = (pos // 30) % len(self.walking_frames_l)
        #     self.image = self.walking_frames_l[frame]
        # else:
            
            
            
        self.collR = False
        self.collL = False

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
                self.collR = True
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
                self.collL = True

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

            if isinstance(block, MovingPlatform):
                self.rect.x += block.change_x
        
        self.NaturalMoving()
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # See if we are on the ground.
        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height
    def jump(self, ignore=False):
        """ Called when user hits 'jump' button. """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT or ignore:
            self.change_y = -5
    def isPosJumping(self):
        front = deepcopy(self.rect)
        front.y -= front.width 
        front.height/=2
        front.x +=10

        sd = pygame.sprite.Sprite()
        sd.rect = front

        r=True
        l=True

        # pygame.draw.rect(self.screen, (0,0,0), front)
        platform_hit_list = pygame.sprite.spritecollide(sd, self.level.platform_list, False)
        if len(platform_hit_list)>0:
            r = False
        front.x-=20
        platform_hit_list = pygame.sprite.spritecollide(sd, self.level.platform_list, False)
        if len(platform_hit_list)>0:
            l = False
        return (l,r)
    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -self.rapidez
        self.direction = "L"

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = self.rapidez
        self.direction = "R"

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
        if self.direction == "R":
            self.direction = "SR"
        elif self.direction == "L":
            self.direction = "SL"
    def NaturalMoving(self):
        self.stop()
    def generateRandMotion(self):
        listMoving = ["L","R", "SR", "SL", "SR", "SL", "SR", "SL"]

        if(pygame.time.get_ticks()-self.randMovingTime>self.randMovingTimeInit):
            direccion = listMoving[randint(0,len(listMoving)-1)]
            if direccion=="L":
                self.go_left()
            elif direccion=="R":
                self.go_right()
            else:
                self.stop()
                self.change_x=0
            self.randMovingTime = randint(200,500)
            if("S" in direccion):
                self.randMovingTime = randint(500,2000)
            self.randMovingTimeInit = pygame.time.get_ticks()


        
    

class Perro(Animal):
    def __init__(self, screen, sprites):
        super().__init__(sprites, "bg.png", screen)
    
    def NaturalMoving(self):
        xA=self.rect.x
        yA=self.rect.y
        xJ=self.player.rect.x
        yJ=self.player.rect.y
        self.stop()
        if distancia_euclidiana(xA+self.rect.width//2, yA+self.rect.height//2, xJ + self.player.rect.width//2, yJ + self.player.rect.height//2)<200:
            if xA<xJ:
                self.go_left()
            else:
                self.go_right()
        if self.isPosJumping()[0] and self.collL or self.isPosJumping()[1] and self.collR:
            self.jump()
        
class Lobo(Animal):
    def __init__(self, screen, sprites):
        super().__init__(("SpritesAnimales/lobo Mexicano/walk.png", "SpritesAnimales/lobo Mexicano/idle.png"), "bg.png", screen)
        self.rapidez = 5
    def NaturalMoving(self):
        self.generateRandMotion()
        if self.isPosJumping()[0] and self.collL or self.isPosJumping()[1] and self.collR:
            self.jump()
        
class Tortuga(Animal):
    def __init__(self, screen, sprites):
        super().__init__(sprites, "bg.png", screen, True)
        self.rapidez = 2
    def NaturalMoving(self):
        self.generateRandMotion()
        


