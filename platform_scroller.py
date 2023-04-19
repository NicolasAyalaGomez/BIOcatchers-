import pygame
import sys
import constants
import levels
from button import Button
from player import Player

from cuerda import Cuerda
from cable import Cable

from particle import Particle

import numpy
import cv2

import math

import random

import threading

from time import sleep as delay

from mapa import Mapa 

from spritesheet_functions import SpriteSheet


cuerdas = []



def distancia_euclidiana(x1, y1, x2, y2):
    distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distancia


def mostrarImagenAtenuada(screen, image, time, p1, pasos):
    for i in range(0, 256, pasos):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((0, 0, 0))
        image.set_alpha(i)
        screen.blit(image, p1)
        pygame.display.flip()
        pygame.time.wait(2)

        
        
    for i in range(time):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()
        pygame.time.wait(1)



    for i in range(255, -1, -pasos):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((0, 0, 0))
        image.set_alpha(i)
        screen.blit(image, p1)
        pygame.display.flip()
        pygame.time.wait(2)
        
    pygame.time.wait(300)


def create_neon(surf, gauss_kernel_size=5, gauss_sigma=5, norm_kernel_size=3):
    surf_alpha = surf.convert_alpha()
    rgb = pygame.surfarray.array3d(surf_alpha)
    alpha = pygame.surfarray.array_alpha(surf_alpha).reshape((*rgb.shape[:2], 1))
    image = numpy.concatenate((rgb, alpha), 2)
    cv2.GaussianBlur(image, ksize=(gauss_kernel_size, gauss_kernel_size), sigmaX=gauss_sigma, sigmaY=gauss_sigma, dst=image)
    cv2.blur(image, ksize=(norm_kernel_size, norm_kernel_size), dst=image)
    bloom_surf = pygame.image.frombuffer(image.flatten(), image.shape[1::-1], 'RGBA')
    return bloom_surf

def obtenerAngulo(p1, p2):

    # Vector que va desde el punto 1 al punto 2
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]

    # Cálculo del ángulo en radianes con respecto al eje horizontal
    angle = math.atan2(dy, dx)

    # Imprime el ángulo en grados
    return math.degrees(angle)
    
def crearChispa(origenX, origenY, direccion, rango, gravity=80):
    colores = [(255, 255, 255), (255, 247, 0), (255, 251, 129)]
    chispa = []
    direccion = (direccion / 180) * math.pi
    rango = (rango / 180) * math.pi
    for i in range(8):
        chispa.append(Particle(origenX,origenY, 1, gravity, colores[random.randint(0,2)] , random.randint(120, 700)))
        angle = random.uniform(direccion-rango* math.pi, direccion+rango * math.pi)
        x_component = math.cos(angle)*80
        y_component = math.sin(angle)*100
        chispa[-1].vx = x_component 
        chispa[-1].vy = y_component
    return chispa


class PuntoDeLuz:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.Enable = True
    def setPosition(self, p1):
        x, y = p1
        self.x = x
        self.y = y
    def getPos(self):
        return (self.x, self.y)

def inicio():
    global clock

    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)


    # ------------------------ carga las imagenes ------------------------

    bioc = pygame.image.load("Pantalla Introduccion/bc-logo.png")
    fasts = pygame.image.load("Pantalla Introduccion/logo-fs.gif")
    elmejorjuego = pygame.image.load("Pantalla Introduccion/spinelogo.gif")
    
    sinp = pygame.image.load("Pantalla Introduccion/ENTER.gif")
    presionaP = pygame.transform.scale(sinp,  (sinp.get_width()//6*4,sinp.get_height()//6*4))
    pantallaInicio = pygame.image.load("Pantalla Introduccion/inicioaaaa.png")


    clavija = pygame.image.load("Pantalla Introduccion/cable.png")
    clavija = pygame.transform.scale(clavija, (clavija.get_width()//11, clavija.get_height()//11))

    clavijaConectada = pygame.image.load("Pantalla Introduccion/poratras.png")
    clavijaConectada = pygame.transform.scale(clavijaConectada, (clavijaConectada.get_width()//13, clavijaConectada.get_height()//13))

    TCorriente = pygame.image.load("Pantalla Introduccion/enchufe.png")
    TCorriente = pygame.transform.scale(TCorriente, (TCorriente.get_width()//11, TCorriente.get_height()//11))

    brillo = pygame.image.load("Pantalla Introduccion/1681184730254.png")
    brillo = pygame.transform.scale(brillo, (brillo.get_width()//200*99-4, brillo.get_height()//20*10+6))

    logos = [pygame.transform.scale(bioc, (bioc.get_width()//2,bioc.get_height()//2)), fasts, elmejorjuego]

    # ------------------------ carga las imagenes ------------------------

    logo_x = constants.SCREEN_WIDTH / 2 
    logo_y = constants.SCREEN_HEIGHT / 2 

        
    # Inicio con logos
    mostrarImagenAtenuada(screen, logos[1], 500, (logo_x - logos[1].get_width() / 2, logo_y - logos[1].get_height() / 2), 4)
    mostrarImagenAtenuada(screen, logos[2], 500, (logo_x - logos[2].get_width() / 2, logo_y - logos[2].get_height() / 2+40), 4)
    mostrarImagenAtenuada(screen, logos[0], 1000, (logo_x - logos[0].get_width() / 2, logo_y - logos[0].get_height() / 2), 2)

    
    pygame.mixer.music.load('Money (2019 Remaster) [8 Bit Tribute to Pink Floyd] - 8 Bit Universe.ogg')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.4)

    SonidoChispa = pygame.mixer.Sound("Pantalla Introduccion/sonido electricidad.wav")


    """ pantalla de inicio """

    image = pygame.Surface((250, 800), pygame.SRCALPHA)

    
    coordenadas = [(105, 100), (101, 100), (93, 100), (89, 100), (85, 100), (81, 100), (77, 100), (73, 100), (69, 100), (65, 100), (57, 100), (53, 100), (49, 100), (45, 100), (45, 99), (45, 95), (45, 91), (45, 87), (45, 83), (45, 79), (45, 75), (45, 71), (45, 67), (45, 63), (45, 59), (45, 55), (45, 51), (45, 47), (45, 43), (45, 43), (49, 43), (53, 43), (53, 43), (53, 47), (53, 51), (53, 55), (53, 59), (53, 63), (53, 67), (53, 71), (53, 75), (53, 79), (53, 83), (109, 99), (109, 
95), (109, 91), (109, 87), (109, 79), (109, 75), (109, 71), (109, 67), (109, 63), (109, 59), (109, 55), (109, 51), (109, 47), (109, 43), (109, 43), (105, 43), (101, 43), (97, 43), (93, 43), (89, 43), (85, 43), (81, 43), (77, 43), (73, 43), (69, 43), (69, 47), (69, 51), (69, 55), (69, 59), (69, 63), (69, 71), (69, 75), (69, 79), (69, 83), (109, 43), (105, 43), (101, 43), (97, 43), (93, 43), (89, 43), (85, 43), (81, 43), (77, 43), (73, 43), (69, 43), (84, 82), (84, 82), (52, 138), (50, 142), (50, 147), (46, 148), (42, 145), (42, 140), (43, 136), (43, 131), (42, 127), (42, 122), (42, 117), (46, 116), (50, 115), (51, 119), (54, 122), (59, 122), (64, 122), (68, 121), (79, 122), (84, 
122), (94, 122), (99, 122), (102, 119), (106, 118), (110, 117), (106, 118), (105, 122), (108, 126), (110, 130), (110, 135), (110, 143), (108, 147), (104, 148), (99, 148), (98, 143), (98, 138), (84, 82), (42, 
218), (47, 218), (52, 218), (57, 218), (62, 218), (66, 219), (71, 219), (78, 219), (83, 219), (87, 218), (93, 218), (98, 218), (103, 218), (109, 218), (108, 214), (107, 210), (108, 206), (104, 204), (99, 201), (99, 196), (99, 191), (100, 182), (104, 179), (109, 179), (108, 175), (108, 170), (108, 165), (104, 164), (99, 164), (94, 165), (89, 164), (86, 161), (81, 161), (76, 161), (72, 162), (67, 162), (62, 162), (52, 162), (47, 162), (46, 166), (43, 170), (43, 175), (42, 179), (46, 181), (51, 181), (52, 185), (51, 189), (50, 193), (51, 197), (52, 201), (46, 201), (44, 205), (43, 209), (44, 205), (44, 200), (42, 161), (42, 166), (77, 164), (68, 164), (84, 82), (43, 235), (43, 240), (43, 245), (43, 250), (42, 254), (42, 259), (42, 264), (42, 269), (42, 274), (42, 279), (43, 283), (48, 283), (52, 282), (52, 277), (51, 273), (51, 268), (51, 263), (51, 258), (51, 252), (52, 247), (53, 243), (53, 238), (57, 236), (61, 238), (66, 238), (72, 238), (78, 236), (83, 236), (87, 235), (94, 235), (90, 236), (86, 237), (92, 237), (98, 237),(106, 239), (103, 243), (107, 244), (108, 240), (107, 235), (104, 238), (100, 241), (97, 245), (97, 250), (98, 254), (99, 258), (102, 261), (106, 260), (109, 263), (110, 272), (110, 277), (110, 282), (42, 300), (43, 304), (44, 308), (44, 313), (44, 318), (49, 318), (52, 315), (52, 310), (56, 309), (61, 309), (66, 309), (70, 310), (69, 314), (68, 318), (66, 322), (69, 
325), (66, 328), (67, 332), (68, 336), (67, 340), (63, 339), (58, 339), (54, 338), (51, 335), (52, 331), (48, 329), (45, 333), (45, 338), (45, 343), (45, 348), (45, 343), (45, 338), (45, 332), (41, 334), (87, 308), (92, 308), (96, 307), (100, 
306), (105, 306), (109, 307), (85, 340), (94, 339), (98, 340), (102, 341), (106, 340), (98, 309), (99, 258), (108, 261), (99, 261), (78, 238), (89, 238), (99, 238), (85, 240), (84, 82), (52, 379), (52, 374), (52, 364), (48, 362), (43, 362), (42, 366), (42, 372), (42, 377), (42, 382), (42, 388), (42, 393), (42, 398), (43, 402), (43, 407), (47, 414), (52, 414), (53, 410), (53, 405), (53, 400), (53, 395), (58, 395), (62, 396), (66, 398), (70, 397), (77, 397), (85, 396), (93, 396), (98, 396), (103, 397), (107, 396), (43, 430), (45, 434), (45, 439), (45, 444), (45, 449), (43, 453), (42, 457), (42, 462), (84, 82), (43, 446), (43, 437), (42, 465), (42, 470), (43, 474), (48, 474), (52, 473), (53, 469), (52, 465), (51, 461), (51, 456), (51, 451), (53, 446), (54, 442), (54, 437), (54, 432), (52, 452), (52, 458), (54, 429), (59, 428), (61, 432), (65, 434), (70, 434), (74, 436), (78, 437), (82, 438), (68, 438), (86, 436), (90, 435), (90, 430), (93, 427), (97, 426), (101, 427), (105, 429), (108, 432), (108, 437), (107, 441), (106, 445), (108, 449), (110, 453), (109, 457), (107, 461), (108, 465), (108, 470), (108, 475), (109, 441), (109, 429), (104, 427), (77, 436), (93, 438), 
(45, 508), (49, 507), (54, 507), (59, 507), (63, 508), (67, 509), (71, 510), (70, 506), (77, 507), (81, 505), (85, 506), (90, 506), (95, 506), (100, 506), (105, 506), (110, 506), (73, 510), (78, 510), (79, 514), (78, 518), (76, 522), (76, 527), (76, 532), (74, 536), (44, 540), (49, 540), (54, 540), (59, 540), (64, 540), (73, 542), (78, 542), (83, 542), (87, 541), (92, 541), (86, 541), (90, 539), (94, 538), (99, 540), (104, 540), (108, 539), (53, 579), (53, 584), (53, 589), (52, 593), (52, 598), (53, 602), (53, 607), (53, 612), (52, 617), (48, 619), (43, 619), (41, 614), (41, 608), (42, 604), (43, 599), (43, 594), (43, 589), (43, 584), (44, 580), (44, 575), (44, 570), (44, 565), (49, 565), (54, 565), (59, 565), (63, 564), (68, 564), (73, 564), (78, 564), (82, 563), (87, 563), (92, 563), (97, 563), (102, 563), (107, 563), (106, 567), (106, 572), (110, 574), (107, 577), (107, 582), (110, 585), (111, 589), (111, 594), (110, 598), (110, 603), (111, 607), (111, 612), (111, 617), (110, 621), (106, 622), (101, 622), (98, 619), (99, 615), (101, 611), (101, 606), (101, 601), (101, 596), (101, 591), (102, 587), (102, 582), (98, 580), (98, 585), (98, 590), (98, 595), (98, 600), (98, 605), (98, 610), (78, 567), (76, 570), (76, 575), (75, 579), (76, 583), (76, 588), (75, 592), (75, 597), (75, 602), (42, 598), (43, 586), (44, 580), (42, 570), (42, 565), (43, 578), (42, 582), (42, 594), (41, 585), (42, 577), (44, 675), (44, 670), (44, 664), (44, 658), (44, 653), (42, 649), (42, 644), (42, 639), (43, 635), (42, 658), (43, 669), (48, 634), (52, 636), (52, 641), (51, 645), (51, 650), (51, 655), (51, 660), (51, 665), (51, 670), (51, 675), (51, 680), (54, 683), (58, 684), (62, 683), 
(66, 682), (70, 680), (70, 675), (68, 671), (67, 667), (68, 662), (69, 658), (70, 654), (70, 648), (70, 643), (70, 638), (86, 642), (84, 646), (82, 650), (86, 653), (91, 652), (96, 652), (102, 652), (106, 653), (106, 658), (107, 662), (108, 666), (109, 670), (110, 674), (110, 679), (107, 682), (102, 682), (99, 685), (99, 679), (99, 674), (98, 670), (108, 652), (113, 659), (45, 724), (45, 729), (45, 739), (45, 745), (46, 749), (52, 748), (54, 744), (54, 739), (54, 734), (59, 734), (64, 734), (68, 735), (72, 737), (73, 733), (78, 733), (82, 734), (88, 734), (92, 732), (98, 732), (103, 731), (107, 730), (108, 726), (107, 722), (108, 717), (109, 713), (110, 709), (110, 704), (109, 699), (103, 698), (99, 697), (98, 702), (100, 706), (100, 711), (100, 716), (78, 730), (73, 730), (62, 730), (58, 729), (84, 730), ]
    coordenadas2 = [(133, 44), (137, 43), (141, 42), (146, 42), (151, 42), (156, 42), (161, 42), (162, 46), (163, 50), (163, 55), (162, 59), (154, 62), (150, 63), (148, 59), (147, 54), (163, 59), (167, 58), (166, 54), (165, 50), (163, 46), (164, 42), (148, 75), (153, 75), (157, 76), (161, 77), (165, 76), (164, 81), (162, 85), (162, 90), (159, 93), (154, 93), (166, 92), (170, 91), (174, 90), (178, 92), (180, 87), (180, 82), (180, 77), (184, 74), (186, 78), (186, 83), 
(186, 88), (183, 91), (180, 94), (131, 117), (133, 121), (134, 126), (134, 131), (134, 136), (132, 116), (138, 117), (142, 118), (147, 118), (152, 118), (156, 116), (160, 115), (164, 117), (150, 117), (150, 122), (149, 126), (148, 130), (148, 
135), (147, 139), (131, 133), (131, 127), (132, 123), (132, 118), (132, 113), (146, 166), (148, 170), (152, 172), (157, 172), (161, 171), (166, 171), (165, 166), (164, 157), (160, 155), (149, 205), (149, 199), (148, 194), (153, 194), (158, 194), (164, 194), (163, 189), (134, 218), (138, 219), (143, 219), (148, 219), (153, 219), (158, 219), (164, 219), (163, 223), (164, 227), (149, 222), (149, 227), (149, 261), (149, 255), (153, 253), (157, 254), (162, 254),
(163, 249), (162, 245), (145, 251), (150, 250), (129, 275), (133, 274), (137, 275), (141, 276), (145, 275), (150, 275), (154, 276), (158, 277), (163, 277), (166, 280), (165, 284), (149, 281), (149, 286), (156, 315), (151, 315), (146, 315), (146, 310), (147, 306), (149, 302), (152, 299), (157, 299), (161, 300), (163, 304), (163, 331), (159, 333), (154, 333), (150, 332), (146, 335), (147, 339), (148, 335), (148, 330), (156, 330), (161, 330), (165, 331), (162, 
357), (158, 356), (154, 354), (150, 355), (148, 359), (149, 363), (150, 367), (153, 370), (158, 370), (163, 370), (163, 375), (157, 375), (153, 374), (147, 374), (146, 370), (146, 365), (146, 360), (148, 356), (152, 354), (157, 354), (162, 355), ]

    luces = []
    luces2 = []

    for i in range(len(coordenadas)):
        x, y = coordenadas[i]
        luces.append(PuntoDeLuz(x,y))
    for i in range(len(coordenadas2)):
        x, y = coordenadas2[i]
        luces2.append(PuntoDeLuz(x,y))

    luces.append(PuntoDeLuz(84,82))
    flag = True

    cable = Cable(30,70)

    drag_start = None
    pos = None

    for luz in luces:
        pygame.draw.circle(image, (102,255,227), luz.getPos(), 10)
    for luz in luces2:
        pygame.draw.circle(image, (77,166,255), luz.getPos(), 8)
    
    neon = create_neon(image, gauss_kernel_size=5, gauss_sigma=15, norm_kernel_size=13)

    conectado = False
    anteriorConectado = False

    pantallaInicio.set_alpha(125)
    presionaP.set_alpha(125)


    chispa = []



    while flag:
        screen.fill((0, 0, 0))
        # Manejar eventos del usuario
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    flag = False
            # Maneja el evento de clic del mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botón izquierdo del mouse
                    drag_start = event.pos

            # Maneja el evento de suelta del mouse
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Botón izquierdo del mouse
                    drag_start = None

            # Comprueba si se está arrastrando
            if drag_start is not None:
                pos = pygame.mouse.get_pos()
        screen.fill((0,0,0))
        screen.blit(pantallaInicio, (0,0))

        image.fill((0,0,0,0))

        


        
        x,y = cable.getPosClavija()
        if drag_start != None:
            pCx = 180+TCorriente.get_width()//2
            pCy = 200+TCorriente.get_height()//2
            if distancia_euclidiana(x,y, drag_start[0], drag_start[1])<15:
                cable.agarrado = True
            if distancia_euclidiana(pos[0],pos[1], pCx,pCy)<TCorriente.get_width():
                cable.setClavPos(pCx, pCy)
                conectado = True
            elif cable.agarrado:
                conectado = False
                cable.setClavPos(pos[0], pos[1])
            # cable.setClavPos(pos[0], pos[1])

            # pCx = 180+TCorriente.get_width()//2
            # pCy = 200+TCorriente.get_height()//2
            # if distancia_euclidiana(x,y, pCx,pCy)<TCorriente.get_width():
            #     cable.setClavPos(pCx, pCy)
            #     print("wfasfa")
            # else:
            #     print("wfasfasdadasda")
            #     cable.setClavPos(pos[0], pos[1])
        else:
            if cable.agarrado and not conectado:
                # cable.setClavPos(pos[0], pos[1])
                cable.devolverGravedad()
            cable.agarrado=False

        screen.blit(TCorriente, (180,200))
        if conectado:
            screen.blit(clavijaConectada, (x-clavijaConectada.get_width()//2,y-clavijaConectada.get_height()//2))
        cable.move(screen)

        
        
        if not conectado:
            pantallaInicio.set_alpha(125)
            presionaP.set_alpha(125)
            screen.blit(pygame.transform.rotate(clavija, -obtenerAngulo(cable.getPunto(-2), cable.getPunto(-1))), (x-clavija.get_width()//2,y-clavija.get_height()//2))
            


        if conectado:
            pantallaInicio.set_alpha(255)
            presionaP.set_alpha(255)
            screen.blit(neon, (0,0))

            screen.blit(brillo, (4,12))

        if not anteriorConectado and conectado:
            SonidoChispa.play(maxtime=random.randint(50,150))
            chispa = crearChispa(pCx,pCy,270,30, gravity=80)


        for par in chispa:
            par.apply_force(0, par.mass * par.gravity)
            par.move(0.1)

            if(par.tiempoDeVida != -1):
                if(pygame.time.get_ticks() - par.nacimiento > par.tiempoDeVida):
                    chispa.remove(par)

            pygame.draw.rect(screen, par.color, (par.x-1, par.y-1, 2,2))
        anteriorConectado = conectado

        pygame.display.update()
        clock.tick(60)


def juegoAsco():
    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    flag = True

    pygame.mixer.music.stop()

    x=0
    y=0

    nava = pygame.image.load("idle_1.png")
    nava = pygame.transform.scale(nava, (50,50))

    meta = pygame.image.load("meta.png")
    meta = pygame.transform.scale(meta, (150,150))

    fondo = pygame.image.load("tlaxcala.png")
    fondo = pygame.transform.scale(fondo, (constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT+100))

    win = pygame.image.load("win.png")
    win = pygame.transform.scale(win, (constants.SCREEN_WIDTH-100, 200))

    vx=0
    vy=0



    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            vy=0
            vx=0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    vy-=4
                if event.key == pygame.K_DOWN:
                    vy+=4
                if event.key == pygame.K_LEFT:
                    vx-=4
                if event.key == pygame.K_RIGHT:
                    vx+=4

        x=x+vx
        y=y+vy
        screen.fill((0,0,0))
        screen.blit(fondo, (0,-50))
        

        if(x>constants.SCREEN_WIDTH-100 and y>constants.SCREEN_HEIGHT-100):
            for i in range(50):
                for i in range(random.randint(10,100)):
                    pygame.time.delay(1)
                    pygame.display.update()
                screen.blit(win, (0,0))
                pygame.display.update()
            flag = False
        else:
            screen.blit(meta, (constants.SCREEN_WIDTH-150, constants.SCREEN_HEIGHT-150))
            screen.blit(nava, (x,y))

        pygame.display.update()
        pygame.time.delay(random.randint(0,20))
        



        
def pausa():
    
    paused = True
    pygame.display.update()

    
    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    
    pygame.mixer.music.pause()
    fontsito = pygame.font.SysFont("Bauhaus 93", 32)    

    screen.fill((50, 50, 50))

    

    menu_text = fontsito.render("Menu Pausa", True, "white")
    menu_rect = menu_text.get_rect(center=(constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/6))

    boton=pygame.image.load("button.png")
    boton=pygame.transform.scale(boton,(200,70))

    play_button = Button(image=boton, pos=(400,170),text_input="Reanudar",font=fontsito,base_color="#3426C3",hovering_color="red")
    pokedex_button = Button(image=boton, pos=(400,270),text_input="pokedex",font=fontsito,base_color="#3426C3",hovering_color="red")
    reiniciar_botton = Button(image=boton, pos=(400,370),text_input="reiniciar",font=fontsito,base_color="#3426C3",hovering_color="red")
    salir_botton = Button(image=boton, pos=(400,470),text_input="salir",font=fontsito,base_color="#3426C3",hovering_color="red")

    

    while True:

          
        while paused == True:

            screen.fill("#808080")

            screen.blit(menu_text, menu_rect)

            play_button.cargar(screen)
            play_button.cambiar_color(pygame.mouse.get_pos())

            pokedex_button.cargar(screen)
            pokedex_button.cambiar_color(pygame.mouse.get_pos())

            reiniciar_botton.cargar(screen)
            reiniciar_botton.cambiar_color(pygame.mouse.get_pos())

            salir_botton.cargar(screen)
            salir_botton.cambiar_color(pygame.mouse.get_pos())

            pygame.display.update()
            
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if play_button.checkForInput(pygame.mouse.get_pos()):

                        paused=False
                        play_button.click(screen)
                        pygame.mixer.music.unpause()
                        return paused
                        

                    elif pokedex_button.checkForInput(pygame.mouse.get_pos()):

                        pokedex_button.click(screen)

                    elif reiniciar_botton.checkForInput(pygame.mouse.get_pos()):
                        reiniciar_botton.click(screen)
                        main()

                    elif salir_botton.checkForInput(pygame.mouse.get_pos()):
                        salir_botton.click(screen)
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

            clock.tick(60)
        
                    


def mostrar_animacion_carga(screen):
    global progreso
    

    bar_x = constants.SCREEN_WIDTH//2-150
    bar_y = 350
    bar_width = 300
    bar_height = 20

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)

    progress = 0

    animacion = []

    # size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    # screen = pygame.display.set_mode(size)

    pygame.init()

    sprite_sheet = SpriteSheet("pantalla de carga/abbeyCatchers.png")
    sprite_sheet.scaled_sprite(3/10)
    # floor = pygame.transform.scale(floor, (floor.get_width()-250, floor.get_height()-50))

    w,h = sprite_sheet.getSize()
    wS = w//4
    for i in range(4):
        image = sprite_sheet.get_image(i*wS, 0, wS, h)
        animacion.append(image)


    pygame.mixer.music.stop()
    fontsito = pygame.font.SysFont("Bauhaus 93", 32) 

    superficie = pygame.Surface((constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT))

    while progress<500:
        if progreso==10:
            progreso = 0
            progress=490
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        superficie.fill((0,0,0))

        # actualizamos la posición de la barra de carga
        progress += 1
        if progress > 500:
            progress = 0

        # dibujamos la barra de carga
        pygame.draw.rect(superficie, WHITE, [bar_x, bar_y, bar_width, bar_height], 2)
        pygame.draw.rect(superficie, WHITE, [bar_x, bar_y, bar_width * (progress / 500), bar_height])
           


    

        menu_text = fontsito.render(str(int(progress/500*100))+"%", True, "white")
        menu_rect = menu_text.get_rect(center=(constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/6*4))
        superficie.blit(menu_text, menu_rect)


        superficie.blit(animacion[(progress//10)%4], (constants.SCREEN_WIDTH//2-wS//2,200))


        screen.blit(superficie, (0,0))

        pygame.display.update()
        clock.tick(60)
    for i in range(255,-1, -1):
        superficie.set_alpha(i)
        screen.fill((0,0,0))
        screen.blit(superficie, (0,0))
        pygame.display.update()
        pygame.time.delay(1)
    pygame.time.delay(200)
    
 
def cargar_niveles():
    global player, current_level_no,level_list,active_sprite_list, screen, progreso, current_level, music_level, mapa
    # Create the player
    player = Player()

    mapa = Mapa(screen)

    # Create all the levels
    level_list = []
    level_list.append(levels.Level_01(player, screen))
    level_list.append(levels.Level_02(player, screen))
    level_list.append(levels.Level_03(player, screen))
    level_list.append(levels.Level_04(player, screen))
    level_list.append(levels.Level_05(player, screen))
    level_list.append(levels.Level_06(player, screen))
    progreso = 10

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]
    music_level = ['The Beatles Lucy in the Sky with Diamonds - 8-Bit Sgt. Pepper.ogg',
                   'The Beatles_ Twist and Shout - Mega Man 2 NES Style Cover [LarryInc64].ogg',
                   'The Beatles - Taxman (8-Bit Version) (1).ogg',
                   'The Beatles - Get Back - Sonic 2 Style [LarryInc64].ogg',
                   'The Beatles_ Back In The USSR - Sonic The Hedgehog 2 Style Cover [LarryInc64].ogg',
                   'Helter Skelter.ogg']

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    player.rect.y = constants.SCREEN_HEIGHT - player.rect.height - 30
    active_sprite_list.add(player)

    # Set a global variable to indicate that the levels and player have been loaded
    global niveles_cargados
    niveles_cargados = True


player = None
current_level_no = None
level_list = None
active_sprite_list = None
progreso = 0
clock = pygame.time.Clock()   
niveles_cargados = False
current_level = None
music_level=None
mapa = None



pygame.init()
pygame.display.set_caption("BIOCATCHERS")
size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)



def main():
    global player, current_level_no,level_list,active_sprite_list, screen, niveles_cargados, current_level, music_level, mapa
    recogerAnimal = False

    
    
    inicio()

    juegoAsco()

    thread = threading.Thread(target=cargar_niveles)
    thread.start()

    mostrar_animacion_carga(screen)
    while not niveles_cargados:
        pygame.display.update
        pygame.time.delay(2)
    
    # Música de fondo
    pygame.mixer.music.load('The Beatles Lucy in the Sky with Diamonds - 8-Bit Sgt. Pepper.ogg')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.4)

    #Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    cPosAnt = 0

    alphaCortina = 255
    

    # -------- Main Program Loop -----------
    while not done:
        animalColl = pygame.sprite.spritecollide(player, player.level.animalList, False)
        if len(animalColl)>0:
            player.printMess("presiona Q para capturar animales", -1)
            recogerAnimal = True
        else:
            player.deleteMessTime(2000)

        for event in pygame.event.get(): # User did something

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pausa()

            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if len(cuerdas)<10:
                        cuerdas.append(Cuerda((108,60,0), (115,115,115), player.rect.x+player.rect.width//2, player.rect.y))
                if event.key == pygame.K_q:
                    if recogerAnimal and len(animalColl)>0:
                        recogerAnimal = False
                        player.capturedAnimals.append(animalColl[0])
                        player.level.animalList.remove(animalColl[0])
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_DOWN :
                    for cuerda in cuerdas:
                        if cuerda.flag: 
                            cuerda.escalando = False
                            player.escalando = False
                
                   
                if event.key == pygame.K_UP:
                    player.jump()
                    for cuerda in cuerdas:
                        if player.escalando == False:
                            cuerda.subirCuerda(player)
                   

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        # Update the player.
        active_sprite_list.update()

        # Update items in the level
        current_level.update()

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.x >= 500:
            diff = player.rect.x - 500
            player.rect.x = 500
            current_level.shift_world(-diff)
        
            for cuerda in cuerdas:
                cuerda.recorrerCuerda(-diff)

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.x <= 120:
            diff = 120 - player.rect.x
            player.rect.x = 120
            current_level.shift_world(diff)


            for cuerda in cuerdas:
                cuerda.recorrerCuerda(diff)

        # If the player gets to the end of the level, go to the next level
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:

            player.rect.x = 120
            player.change_x = 0
            
            if current_level_no < len(level_list)-1:
                if(len(player.capturedAnimals)==current_level.animalN):
                    current_level_no += 1
                    mapa.Pines[0][1]=True
                    player.printMess("Haz completado el primer nivel. ¡Bien hecho!", 4000)
                else:
                    player.rect.x = 120
                    current_level.shift_world(480)
                    player.rect.x = 499
                    for cuerda in cuerdas:
                        cuerda.recorrerCuerda(480)
                    player.printMess("Tienes que recoger a todos los animales para continuar", 4000)
                
                current_level = level_list[current_level_no]
                player.level = current_level
                mapa.Mostrar(player)
                pygame.mixer.music.load(music_level[current_level_no])
                pygame.mixer.music.play(0)
                pygame.mixer.music.set_volume(0.4)

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        

        flag = False

        for cuerda in cuerdas:
            cuerda.flag = False
            cuerda.move(screen, player)

 
        for cuerda in cuerdas:
            cuerda.phisics(player, current_position, cPosAnt)

        # print(current_position, " ", particles[12].x)
        cPosAnt = current_position

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
        active_sprite_list.draw(screen)

        player.updateMess()
        

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # print(player.direction)

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()
    

if __name__ == "__main__":
    main()

